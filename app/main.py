from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.auth.models import Base
from app.auth.redis import init_redis
from app.auth.routes import router as auth_router
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI, yiel=None):
    # --- Startup ---
    # This line creates all tables defined in your models if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await init_redis()
    yiel

    yield  # The app stays "here" while running

    # --- Shutdown ---
    # (Optional: Close Redis connection here if you like)
    # from app.db.redis import redis_client
    # if redis_client:
    #     await redis_client.close()


app = FastAPI(
    title="TenantHub API",
    lifespan=lifespan  # Connect the lifespan to the app
)

# Include your routes
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "TenantHub API running"}