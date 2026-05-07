from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    REDIS_URL: str
    EXPIRES_IN: int = 86400

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()