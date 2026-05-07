from datetime import datetime, timedelta, timezone
import re

from fastapi import HTTPException, status

from app.auth.auth_utils import hash_password, verify_password
from app.auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.auth.repository import (
    UserRepository,
    TenantRepository,
    RefreshTokenRepository,
)


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


class AuthService:
    def __init__(self, db, redis=None):
        self.db = db
        self.redis = redis

        self.user_repo = UserRepository(db)
        self.tenant_repo = TenantRepository(db)
        self.refresh_repo = RefreshTokenRepository(db)

    async def register(self, data):
        slug = slugify(data.tenant.name)

        tenant = await self.tenant_repo.get_by_slug(slug)
        if not tenant:
            tenant = await self.tenant_repo.create(data.tenant.name, slug)

        existing = await self.user_repo.get_by_email(data.email, tenant.id)
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        user = await self.user_repo.create(
            email=data.email,
            username=data.email.split("@")[0],
            hashed_password=hash_password(data.password),
            tenant_id=tenant.id,
            full_name=data.full_name,
        )

        access_token = create_access_token({
            "user_id": user.id,
            "tenant_id": tenant.id,
        })

        refresh_token = create_refresh_token({
            "user_id": user.id,
        })

        await self.refresh_repo.create(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )

        await self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def login(self, email: str, password: str, tenant_id: int):
        user = await self.user_repo.get_by_email(email, tenant_id)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token = create_access_token({
            "user_id": user.id,
            "tenant_id": tenant_id,
        })

        refresh_token = create_refresh_token({
            "user_id": user.id,
        })

        await self.refresh_repo.create(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )

        await self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh(self, refresh_token: str):
        payload = verify_token(refresh_token, expected_type="refresh")

        stored = await self.refresh_repo.get(refresh_token)
        if not stored or stored.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        new_access = create_access_token({
            "user_id": stored.user_id,
        })

        new_refresh = create_refresh_token({
            "user_id": stored.user_id,
        })

        stored.is_revoked = True

        await self.refresh_repo.create(
            user_id=stored.user_id,
            token=new_refresh,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )

        await self.db.commit()

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
            "token_type": "bearer",
        }

    async def logout(self, refresh_token: str):
        stored = await self.refresh_repo.get(refresh_token)

        if not stored:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        stored.is_revoked = True
        await self.db.commit()

        return {"message": "Logged out successfully"}