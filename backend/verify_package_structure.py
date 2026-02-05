#!/usr/bin/env python3
"""
Verification script to check if the backend package structure is correct
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the path temporarily for this check
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

def verify_package_structure():
    """Verify that the backend package structure is correct"""
    print("Verifying backend package structure...")

    # Check if app directory exists
    app_dir = backend_path / "app"
    if not app_dir.exists():
        print("❌ Error: app/ directory does not exist")
        return False

    print("✅ app/ directory exists")

    # Check if app/__init__.py exists
    app_init = app_dir / "__init__.py"
    if not app_init.exists():
        print("❌ Error: app/__init__.py does not exist")
        return False

    print("✅ app/__init__.py exists")

    # Check if app/main.py exists
    main_py = app_dir / "main.py"
    if not main_py.exists():
        print("❌ Error: app/main.py does not exist")
        return False

    print("✅ app/main.py exists")

    # Try to import the app module
    try:
        from app.main import app
        print("✅ Successfully imported app from app.main")

        # Check if app is a FastAPI instance
        try:
            from fastapi import FastAPI
            if isinstance(app, FastAPI):
                print("✅ app is a FastAPI instance")
            else:
                print("⚠️  app is not a FastAPI instance")
        except ImportError:
            print("⚠️  Could not verify if app is a FastAPI instance (FastAPI not available)")

    except ImportError as e:
        print(f"❌ Failed to import app from app.main: {e}")
        return False

    # Check the content of main.py for the app assignment
    main_content = main_py.read_text()
    if "app =" in main_content:
        print("✅ app variable is defined in main.py")
    else:
        print("❌ app variable is not defined in main.py")

    print("\nPackage structure verification completed successfully!")
    print("The backend should be able to start without 'ModuleNotFoundError: No module named app'")

    return True

if __name__ == "__main__":
    success = verify_package_structure()
    if not success:
        print("\n❌ Package structure verification failed!")
        sys.exit(1)
    else:
        print("\n✅ Package structure is correct!")