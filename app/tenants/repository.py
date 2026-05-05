from sqlalchemy import select
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from .models import Tenant


class TenantRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_slug(self, slug: str) -> Optional[Tenant]:
        result = await self.session.execute(
            select(Tenant).where(Tenant.slug == slug)
        )
        return result.scalars().first()

    async def create_tenant(self, name: str, slug: str) -> Tenant:
        tenant = Tenant(
            name=name,
            slug=slug
        )

        self.session.add(tenant)
        await self.session.flush()
        return tenant