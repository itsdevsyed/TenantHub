from pydantic import BaseModel, EmailStr


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