from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.auth.models import User, Tenant


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str, tenant_id: int):
        res = await self.db.execute(
            select(User).where(
                User.email == email,
                User.tenant_id == tenant_id
            )
        )
        return res.scalars().first()

    async def create(self, **data):
        user = User(**data)
        self.db.add(user)
        await self.db.flush()
        return user


class TenantRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_slug(self, slug: str):
        res = await self.db.execute(
            select(Tenant).where(Tenant.slug == slug)
        )
        return res.scalars().first()

    async def create(self, name: str, slug: str):
        t = Tenant(name=name, slug=slug)
        self.db.add(t)
        await self.db.flush()
        return t