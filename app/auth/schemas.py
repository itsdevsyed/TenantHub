from pydantic import BaseModel, EmailStr
from typing import Optional


class TenantCreate(BaseModel):
    name: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    tenant: TenantCreate


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ---------------- TOKENS ----------------

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    pass

class LogoutRequest(BaseModel):
    pass  