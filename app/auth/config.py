from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:syed@127.0.0.1:5432/TenantHub"
    ALEMBIC_DATABASE_URL: ClassVar[str] = "postgresql://postgres:syed@localhost:5432/TenantHub"

    JWT_SECRET: str = "supersecret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # Modern Pydantic V2 configuration
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()