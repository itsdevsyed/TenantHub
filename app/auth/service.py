import re
from fastapi import HTTPException
from app.auth.auth_utils import hash_password, verify_password
from app.auth.jwt_handler import create_token
from app.auth.repository import UserRepository, TenantRepository


def slugify(name: str):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


class AuthService:
    def __init__(self, db, redis=None):
        self.db = db
        self.redis = redis
        self.user_repo = UserRepository(db)
        self.tenant_repo = TenantRepository(db)

    async def register(self, data):

        slug = slugify(data.tenant.name)

        tenant = await self.tenant_repo.get_by_slug(slug)
        if not tenant:
            tenant = await self.tenant_repo.create(data.tenant.name, slug)

        existing = await self.user_repo.get_by_email(data.email, tenant.id)
        if existing:
            raise HTTPException(400, "User exists")

        user = await self.user_repo.create(
            email=data.email,
            username=data.email.split("@")[0],
            hashed_password=hash_password(data.password),
            tenant_id=tenant.id,
            full_name=data.full_name
        )

        await self.db.commit()

        return {
            "refresh_token": create_token({
                "user_id": user.id,
                "tenant_id": tenant.id
            }),

            "access_token": create_token({
                "user_id": user.id,
                "tenant_id": tenant.id
            })
        }

    async def login(self, email: str, password: str, tenant_id: int):

        user = await self.user_repo.get_by_email(email, tenant_id)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(401, "Invalid credentials")

        return {
            "refresh_token": create_token({
                "user_id": user.id,
                "tenant_id": tenant_id
            }),
            "access_token": create_token({
                "user_id": user.id,
                "tenant_id": tenant_id
            })
        }