from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_TOKEN_URL: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DEBUG: bool
    TESTING: bool
    LOG_DIR: str
    LOG_LEVEL: str

    class Config:
        env_file = ".env"


settings = Settings()
