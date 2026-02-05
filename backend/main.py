import os
import sys
import logging
from typing import Optional
from datetime import datetime
import uuid

# Add the parent directory (project root) to Python path so 'backend' package can be found
# This handles the case when running with uvicorn from the project root: uvicorn backend.main:app
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # This is the project root
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field
from app.models.user import User
from app.models.task import Task
from config.database import engine, settings
from contextlib import contextmanager






# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    app = FastAPI(
        title="Todo API",
        description="A secure, stateless backend API for a multi-user Todo application",
        version="1.0.0",
    )

    # Add CORS middleware to allow frontend to communicate with backend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include authentication routes
    import sys
    import os

    # Add the project root and backend directory to the path to resolve imports properly
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_file_dir)

    # Add parent directory (project root) to path
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    # Add backend directory to path as well
    if current_file_dir not in sys.path:
        sys.path.insert(0, current_file_dir)

    try:
        from api.v1.auth import router as auth_router
    except ImportError:
        try:
            from backend.api.v1.auth import router as auth_router
        except ImportError:
            # Fallback: add project root to path and try again
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            from backend.api.v1.auth import router as auth_router

    app.include_router(auth_router, prefix="/auth", tags=["auth"])

    # Include task routes - ensure app module can be found
    try:
        from app.api.v1.endpoints.tasks import router as tasks_router
    except ImportError:
        try:
            from backend.app.api.v1.endpoints.tasks import router as tasks_router
        except ImportError:
            # Add project root and try again
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            from backend.app.api.v1.endpoints.tasks import router as tasks_router

    app.include_router(tasks_router, prefix="/api/v1", tags=["tasks"])

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "version": "1.0.0"}

    @app.on_event("startup")
    def on_startup():
        """
        Create all database tables on application startup
        """
        logger.info("Creating database tables...")
        try:
            # Import all models to ensure they're registered with SQLModel metadata
            from app.models.user import User
            from app.models.task import Task

            # Create all SQLModel tables to ensure schema is up to date
            # Don't drop tables in production, only create new ones
            from sqlmodel import SQLModel
            SQLModel.metadata.create_all(engine)
            logger.info("Application started successfully")
        except Exception as e:
            logger.error(f"Error during startup: {e}")
            raise

    # Protected route example - import after dependencies are available
    try:
        from auth.dependencies import get_current_user
        from schemas.user import TokenData
    except ImportError:
        try:
            from backend.auth.dependencies import get_current_user
            from backend.schemas.user import TokenData
        except ImportError:
            # Add the project root to the path to make absolute imports work
            import sys
            import os
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up to project root
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            from backend.auth.dependencies import get_current_user
            from backend.schemas.user import TokenData

    @app.get("/users/me")
    def read_users_me(current_user: TokenData = Depends(get_current_user)):
        return current_user

    return app


app = create_app()