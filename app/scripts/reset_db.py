import asyncio

from app.db.base import Base
from app.db.session import engine

# IMPORTANT: import all models so they register on Base
from app.auth import models as auth_models


async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("DB reset completed")


if __name__ == "__main__":
    asyncio.run(reset_db())