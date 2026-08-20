from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from prometheus_fastapi_instrumentator import Instrumentator

from app.db.base import Base
from app.db.session import engine, get_db
from prometheus_fastapi_instrumentator import Instrumentator

from app.auth.models import Tenant, User, RefreshToken
from app.auth.routes import router as auth_router
from app.auth.redis import get_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
<<<<<<< HEAD
Instrumentator().instrument(app).expose(app)
app.include_router(auth_router)
@app.get("/")
async def root():
    return {"message": "TenantHub API is running"}
=======

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

# API routes
app.include_router(auth_router)
@app.get("/test-error")
def test_error():
    raise Exception("Intentional test error")
>>>>>>> 619bd27 (added the grafana+ loki+ promethius config to setup)

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
