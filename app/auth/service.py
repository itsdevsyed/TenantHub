import time
from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, status
from fastapi.concurrency import run_in_threadpool  # For non-blocking CPU work
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from . import schemas
from .config import settings
from .jwt_handler import create_access_token, create_refresh_token, verify_access_token
from .repository import UserRepository, TenantRepository

# Password hashing configuration (Argon2 is secure but slow by design)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class AuthService:
    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.user_repo = UserRepository(session)
        self.tenant_repo = TenantRepository(session)
        self.redis = redis

    async def hash_password(self, password: str) -> str:
        """Runs the expensive hashing in a background thread."""
        return await run_in_threadpool(pwd_context.hash, password)

    async def verify_password(self, plain: str, hashed: str) -> bool:
        """Runs the expensive verification in a background thread."""
        return await run_in_threadpool(pwd_context.verify, plain, hashed)

    # ---------------- Blacklist JWT ----------------
    async def blacklist_token(self, token: str):
        try:
            payload = verify_access_token(token)
            exp = payload.get("exp")
            ttl = int(exp - time.time())
            if ttl > 0:
                await self.redis.setex(f"bl_{token}", ttl, "true")
        except Exception as e:
            print(f"Error blacklisting token: {e}")

    # ---------------- Register User ----------------
    async def register_user(self, data: schemas.UserCreate):
        # 1. Check existing user
        start_db = time.perf_counter()
        existing_user = await self.user_repo.get_by_email(str(data.email))
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        print(f">>> DB User Check took: {time.perf_counter() - start_db:.4f}s")

        # 2. Check or create tenant
        start_tenant = time.perf_counter()
        tenant_name = data.tenant.name
        tenant = await self.tenant_repo.get_by_name(tenant_name)
        if not tenant:
            tenant = await self.tenant_repo.create_tenant(tenant_name)
        print(f">>> Tenant Logic took: {time.perf_counter() - start_tenant:.4f}s")

        # 3. Hash password (CPU Intensive)
        start_hash = time.perf_counter()
        hashed_pw = await self.hash_password(data.password)
        print(f">>> Password Hashing took: {time.perf_counter() - start_hash:.4f}s")

        # 4. Create User and Commit
        start_commit = time.perf_counter()
        user = await self.user_repo.create_user(
            email=str(data.email),
            hashed_password=hashed_pw,
            tenant_id=tenant.id,
            full_name=data.full_name
        )
        await self.session.commit()
        print(f">>> DB Commit took: {time.perf_counter() - start_commit:.4f}s")

        # 5. Generate JWT tokens
        access = create_access_token({"sub": str(user.id), "tenant_id": tenant.id})
        refresh = create_refresh_token({"sub": str(user.id), "tenant_id": tenant.id})

        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer"
        }

    # ---------------- Login User ----------------
    async def login_user(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)

        # Verify password (using the async wrapper)
        if not user or not await self.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access = create_access_token({"sub": str(user.id), "tenant_id": user.tenant_id})
        refresh = create_refresh_token({"sub": str(user.id), "tenant_id": user.tenant_id})

        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer"
        }