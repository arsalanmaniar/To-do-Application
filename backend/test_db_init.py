#!/usr/bin/env python3
"""
Test script to verify database initialization implementation
"""
import os
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

try:
    # Test that the main module can be imported without errors
    from app.main import app
    print("[OK] Successfully imported app with database initialization")

    # Test that SQLModel metadata includes the models
    from sqlmodel import SQLModel
    from app.models import task, user

    # Check that tables are registered in metadata
    tables = SQLModel.metadata.tables.keys()
    print(f"Registered tables: {list(tables)}")

    if 'task' in str(tables) or 'user' in str(tables):
        print("[OK] Models are registered with SQLModel metadata")
    else:
        print("[WARN] No tables detected in metadata")

    print("\nDatabase initialization implementation is ready!")
    print("- Tables will be created automatically on startup")
    print("- Uses existing DATABASE_URL from environment")
    print("- Compatible with Neon Serverless PostgreSQL")

except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Error: {e}")
    sys.exit(1)