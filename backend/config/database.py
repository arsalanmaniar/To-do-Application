"""
Database configuration for the authentication backend.
Configures SQLAlchemy engine for Neon Serverless PostgreSQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import os


from pydantic import Field

class Settings(BaseSettings):
    database_url: str
    secret_key: str = Field(..., alias="BETTER_AUTH_SECRET")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


def get_database_url():
    """Get database URL from environment, with fallback for migrations."""
    # First try to get from environment variable
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url

    # For migrations, we can create a dummy URL if needed
    # This is safe to do as long as we don't actually connect during migration generation
    return "postgresql://user:password@localhost/dbname"


def get_settings():
    """Get settings, with fallback for migration scenarios."""
    try:
        return Settings()
    except Exception:
        # If settings can't be loaded (e.g., during migration generation),
        # return a minimal configuration that allows model loading
        class DummySettings:
            database_url = get_database_url()
            secret_key = os.getenv("SECRET_KEY", "dummy-secret-key-for-migrations")
            algorithm = "HS256"
            access_token_expire_minutes = 30

        return DummySettings()


settings = get_settings()


# Create the database engine with appropriate settings based on database type
if settings.database_url.startswith("sqlite"):
    # SQLite settings
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},  # Required for SQLite
        echo=False  # Set to True for debugging SQL queries
    )
else:
    # PostgreSQL settings (including Neon)
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=300,
        echo=False  # Set to True for debugging SQL queries
    )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()