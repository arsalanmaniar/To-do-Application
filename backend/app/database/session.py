from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the database engine
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,  # Set to True for SQL query logging
    pool_pre_ping=True,     # Verify connections before use
    pool_recycle=300,       # Recycle connections after 5 minutes
)

# Create the session maker using SQLModel Session
SessionLocal = sessionmaker(class_=Session, autocommit=False, autoflush=False, bind=engine)


def get_session():
    """
    Dependency to get a database session
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()