from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    database_url: str
    better_auth_secret: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    db_echo: bool = False  # Set to True to log SQL queries

    class Config:
        env_file = ".env"


settings = Settings()