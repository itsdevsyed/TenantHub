from fastapi import APIRouter, Depends
from app.auth.schemas import UserCreate, UserLogin
from app.auth.dependencies import get_auth_service

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(payload: UserCreate, service=Depends(get_auth_service)):
    return await service.register(payload)


@router.post("/login")
async def login(
    payload: UserLogin,
    tenant_id: int,
    service=Depends(get_auth_service)
):
    return await service.login(payload.email, payload.password, tenant_id)