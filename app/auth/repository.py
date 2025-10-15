from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import  select
from . import models
from typing import Optional

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self,email:str) -> Optional[models.User]:
        q = await self.session.execute(select(models.User).filter(models.User.email == email))
        return q.scalar().first()

    async def create_user(self, email: str, hashed_password: str, tenant_id: int, full_name: str = None):
        user  = models.User(
            email=email,
            hashed_password=hashed_password,
            tenant_id=tenant_id,
            full_name = full_name
        )
        self.session.add(user)
        await self.session.flush()
        return user



class TenantRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self , name:str) -> Optional[models.Tenant]:
        result = await self.session.execute(
            select(models.Tenant).filter(models.Tenant.name == name)
        )
        return result.scalar().first()

    async def create_tenant(self, name: str, tenant_id: int, full_name: str = None):
        tenant = models.Tenant(name = name)
        self.session.add(tenant)
        await self.session.flush()
        return tenant



















