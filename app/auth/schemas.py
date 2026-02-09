from pydantic import BaseModel, EmailStr
from typing import Optional

class TennantCreate(BaseModel):
    name:str


class UserCreate(BaseModel):
    email:EmailStr
    password:str
    full_name:Optional[str] = None
    tenant:TennantCreate


class Token(BaseModel):
    access_token:str
    token_type:str = "bearer"
    refresh_token:Optional[str] = None

class TokenPayload(BaseModel):
    sub:str
    tenant_id:int


class UserLogin(BaseModel):
    email: EmailStr
    password: str

