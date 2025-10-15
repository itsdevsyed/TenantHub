from typing import ClassVar
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:syed@localhost:5432/TenantHub"  # FastAPI runtime
    ALEMBIC_DATABASE_URL: ClassVar[str] = "postgresql://postgres:syed@localhost:5432/TenantHub"  # Alembic migrations
    JWT_SECRET: str = "supersecret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = ".env"

settings = Settings()
