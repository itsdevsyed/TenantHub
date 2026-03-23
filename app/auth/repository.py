from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models
from typing import Optional


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[models.User]:
        # Using .execute() + .scalars().first() is correct for SQLAlchemy 2.0 Async
        result = await self.session.execute(
            select(models.User).filter(models.User.email == email)
        )
        return result.scalars().first()

    # --- ADDED THIS METHOD ---
    async def get_by_id(self, user_id: int) -> Optional[models.User]:
        """Required for the /me route and get_current_user dependency"""
        result = await self.session.execute(
            select(models.User).filter(models.User.id == user_id)
        )
        return result.scalars().first()

    async def create_user(
        self, email: str, hashed_password: str, tenant_id: int, full_name: str = None
    ) -> models.User:
        user = models.User(
            email=email,
            hashed_password=hashed_pw,
            tenant_id=tenant_id,
            full_name=full_name
        )
        self.session.add(user)
        # flush() pushes the object to the DB so we get the ID back,
        # but doesn't finish the transaction yet.
        await self.session.flush()
        return user


class TenantRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, name: str) -> Optional[models.Tenant]:
        result = await self.session.execute(
            select(models.Tenant).filter(models.Tenant.name == name)
        )
        return result.scalars().first()

    async def create_tenant(self, name: str) -> models.Tenant:
        tenant = models.Tenant(name=name)
        self.session.add(tenant)
        await self.session.flush()
        return tenant