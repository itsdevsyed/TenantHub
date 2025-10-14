from pydantic import  BaseSettings

class Settings(BaseSettings):

    DATABASE_URL:str
    JWT_SECRET:str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 15
    REFRESH_TOKEN_MINUTES : int = 60 * 25 * 7


    class Config:
        env_file = ".env"


settings = Settings()