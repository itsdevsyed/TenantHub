from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import schemas
from app.auth.dependencies import get_auth_service, get_current_user
from app.auth.service import AuthService
from app.auth.models import User
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(
    payload: schemas.UserCreate,
    service: AuthService = Depends(get_auth_service)
):
    return await service.register(payload)


@router.post("/login")
async def login(
    payload: schemas.UserLogin,
    tenant_id: int,
    service: AuthService = Depends(get_auth_service)
):
    return await service.login(payload.email, payload.password, tenant_id)

@router.post("/refresh")
async def refresh(
    authorization: str = Header(...),
    service: AuthService = Depends(get_auth_service)
):
    try:
        token = authorization.replace("Bearer ", "")
        return await service.refresh(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.get("/me")
async def me(
    current=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.id == current["user_id"])
    )
    user = result.scalars().first()

    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "tenant_id": user.tenant_id
    }

@router.post("/logout")
async def logout(
    authorization: str = Header(...),
    service: AuthService = Depends(get_auth_service)
):
    try:
        token = authorization.replace("Bearer ", "")
        return await service.logout(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")