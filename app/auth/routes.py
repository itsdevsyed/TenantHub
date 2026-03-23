from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.db.session import get_db
from .dependencies import get_current_user, oauth2_scheme
from .redis import get_redis
from . import schemas, models
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

@router.get("/me", response_model=schemas.UserResponse)
async def get_me(current_user: models.User = Depends(get_current_user)):
    """Fetches the currently logged-in user's profile"""
    return current_user

@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service)
):
    """Blacklists the current token in Redis"""
    await service.blacklist_token(token)
    return {"message": "Successfully logged out"}