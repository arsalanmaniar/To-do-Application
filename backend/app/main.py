from fastapi import FastAPI
from sqlmodel import SQLModel
from app.api.v1.endpoints import tasks
from app.core.config import settings
from app.database.session import engine
from app import models  # Import all models to register them with SQLModel
from app.core.logging import logger


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    app = FastAPI(
        title="Todo API",
        description="A secure, stateless backend API for a multi-user Todo application",
        version="1.0.0",
    )

    # Include API routes
    app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "version": "1.0.0"}

    @app.on_event("startup")
    def on_startup():
        """
        Create all database tables on application startup
        """
        logger.info("Initializing database tables...")
        try:
            SQLModel.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise

    return app


app = create_app()