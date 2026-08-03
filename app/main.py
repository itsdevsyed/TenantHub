from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

# Import models so SQLAlchemy creates the tables
from app.auth.models import Tenant, User, RefreshToken

# Import the router
from app.auth.routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="TenantHub API",
    lifespan=lifespan,
)

# Register routes
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "TenantHub API is running "}
