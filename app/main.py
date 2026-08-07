from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.db.base import Base
from app.db.session import engine, get_db

from app.auth.models import Tenant, User, RefreshToken
from app.auth.routes import router as auth_router
from app.auth.redis import get_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)


@app.get("/health", tags=["Health"])
async def health(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    try:
        await db.execute(text("SELECT 1"))
        await redis.ping()

        return {
            "status": "healthy",
            "database": "up",
            "redis": "up",
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
        }
