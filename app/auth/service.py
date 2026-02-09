from datetime import timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from yt_dlp.utils import jwt_encode

from . import schemas
from .config import settings
from .jwt_handler import create_access_token, create_refresh_token
from .repository import UserRepository, TenantRepository

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


class AuthService:
    def __init__(self, session: AsyncSession, redis):
        self.session = session
        self.user_repo = UserRepository(session)
        self.tenant_repo = TenantRepository(session)
        self.redis = redis



    async def blacklist_token(self,token:str):
        try:
            payload = jwt_encode(token, settings.JWT_SECRET)
            exp = payload.get("exp")
            ttl = int(exp - (timedelta(seconds=0).total_seconds()))
            await self.redis.setex(f"bl_{token}", ttl, "true")
        except Exception as e:
            print(e)

    # Hash password

    # Verify password

    # ---------------- Register ----------------
    async def register_user(self, data: schemas.UserCreate):
        existing_user = await self.user_repo.get_by_email(str(data.email))
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        tenant = await self.tenant_repo.get_by_name(data.tenant.name)
        if not tenant:
            tenant = await self.tenant_repo.create_tenant(data.tenant.name)

        hashed_pw = hash_password(data.password)
        user = await self.user_repo.create_user(
            email=str(data.email),
            hashed_password=hashed_pw,
            tenant_id=tenant.id,
            full_name=data.full_name
        )

        await self.session.commit()
        access = create_access_token({"sub": str(user.id), "tenant_id": tenant.id})
        refresh = create_refresh_token({"sub": str(user.id), "tenant_id": tenant.id})

        return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

    # ---------------- Login ----------------
    async def login_user(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access = create_access_token({"sub": str(user.id), "tenant_id": user.tenant_id})
        refresh = create_refresh_token({"sub": str(user.id), "tenant_id": user.tenant_id})
        return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}
