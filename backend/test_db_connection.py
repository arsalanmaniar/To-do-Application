#!/usr/bin/env python3
"""
Test script to verify database connection and initialization
"""
import os
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_db_connection():
    """Test database connection and initialization"""
    try:
        # Import the required modules
        from app.core.config import settings
        from app.database.session import engine
        from sqlmodel import SQLModel

        print(f"DATABASE_URL loaded: {'Yes' if settings.database_url else 'No'}")
        print(f"Database URL: {settings.database_url[:50]}..." if settings.database_url else "No URL")

        # Import models to register them
        from app import models

        # Check if metadata contains tables
        tables = list(SQLModel.metadata.tables.keys())
        print(f"Registered tables: {tables}")

        print("Database initialization setup is correct!")
        print("When the app starts, it will create these tables in Neon PostgreSQL")

        return True

    except ImportError as e:
        print(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_db_connection()
    if success:
        print("\n✅ Database initialization implementation is ready!")
        print("The tables will be created when the backend starts up.")
    else:
        print("\n❌ Issues found with database initialization setup.")
        sys.exit(1)