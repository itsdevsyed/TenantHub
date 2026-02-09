from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db
from . import schemas
from .service import AuthService

router = APIRouter(tags=["Auth"])

@router.post("/register")
async def register_user(payload: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.register_user(payload)

@router.post("/login")
async def login_user(payload: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login_user(payload.email, payload.password)
