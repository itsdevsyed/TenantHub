from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.db.session import get_db
from .redis import get_redis
from . import schemas
from .service import AuthService

router = APIRouter(tags=["Auth"])

def get_auth_service(
    db: AsyncSession = Depends(get_db),
    redis_conn: Redis = Depends(get_redis) # Using 'Redis' as type hint
) -> AuthService:
    return AuthService(db, redis_conn)

@router.post("/register")
async def register_user(
    payload: schemas.UserCreate,
    service: AuthService = Depends(get_auth_service)
):
    return await service.register_user(payload)

@router.post("/login")
async def login_user(
    payload: schemas.UserLogin,
    service: AuthService = Depends(get_auth_service)
):
    return await service.login_user(payload.email, payload.password)