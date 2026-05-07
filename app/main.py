from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

# IMPORTANT
from app.auth.models import Tenant, User, RefreshToken


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)