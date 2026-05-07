from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.auth.models import User, Tenant, RefreshToken


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str, tenant_id: int):
        result = await self.db.execute(
            select(User).where(
                User.email == email,
                User.tenant_id == tenant_id
            )
        )
        return result.scalars().first()

    async def create(self, **data):
        user = User(**data)
        self.db.add(user)
        await self.db.flush()
        return user


class TenantRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_slug(self, slug: str):
        result = await self.db.execute(
            select(Tenant).where(Tenant.slug == slug)
        )
        return result.scalars().first()

    async def create(self, name: str, slug: str):
        tenant = Tenant(name=name, slug=slug)
        self.db.add(tenant)
        await self.db.flush()
        return tenant


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, token: str, expires_at):
        refresh = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        self.db.add(refresh)
        await self.db.flush()
        return refresh

    async def get(self, token: str):
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        return result.scalars().first()

    async def revoke(self, token: str):
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        refresh = result.scalars().first()

        if refresh:
            refresh.is_revoked = True
            await self.db.flush()

        return refresh