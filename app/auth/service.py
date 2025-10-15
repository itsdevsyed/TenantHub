from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import UserRepository, TenantRepository
from .jwt_handler import create_access_token, create_refresh_token
from . import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.tenant_repo = TenantRepository(session)

    # Hash password
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    # Verify password
    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    # ---------------- Register ----------------
    async def register_user(self, data: schemas.UserCreate):
        existing_user = await self.user_repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        tenant = await self.tenant_repo.get_by_name(data.tenant.name)
        if not tenant:
            tenant = await self.tenant_repo.create_tenant(data.tenant.name)

        hashed_pw = self.hash_password(data.password)
        user = await self.user_repo.create_user(
            email=data.email,
            hashed_password=hashed_pw,
            tenant_id=tenant.id,
            full_name=data.full_name
        )

        await self.session.commit()
        access = create_access_token({"sub": str(user.id), "tenant_id": tenant.id})
        refresh = create_refresh_token({"sub": str(user.id), "tenant_id": tenant.id})

        return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

    # ---------------- Login ----------------
    async def login_user(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access = create_access_token({"sub": str(user.id), "tenant_id": user.tenant_id})
        refresh = create_refresh_token({"sub": str(user.id), "tenant_id": user.tenant_id})
        return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}
