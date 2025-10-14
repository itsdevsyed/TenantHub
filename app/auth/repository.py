from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import  select
from . import models
from typing import Optional

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self,email:str) -> Optional[models.User]:
        q = await self.session.execute(select(models.User).where(models.User.email == email))
