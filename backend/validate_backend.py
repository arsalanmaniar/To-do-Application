#!/usr/bin/env python
"""
Validate that the backend structure is correct and all imports work.
"""
import os
import sys
from pathlib import Path

def validate_backend_structure():
    """Validate the backend structure and imports."""
    print("[INFO] Validating backend structure...")

    # Get the project root (parent of current backend directory)
    current_dir = Path(__file__).parent
    project_root = current_dir.parent  # Go up one level to project root

    print(f"[INFO] Project root: {project_root}")
    print(f"[INFO] Current backend path: {current_dir}")

    # Add project root to Python path so 'backend' package can be found
    sys.path.insert(0, str(project_root))

    # Test importing the main app
    try:
        print("\n[TEST] Testing main app import...")

        # Import the main module using absolute imports
        from backend import main
        print("[SUCCESS] Main app imported successfully")
        print(f"   Title: {main.app.title}")
        print(f"   Description: {main.app.description}")

        # Check if routes are loaded
        auth_routes = [route for route in main.app.routes if hasattr(route, 'path') and '/auth' in str(route.path)]
        print(f"[SUCCESS] Found {len(auth_routes)} authentication routes")

        # Check for other important routes
        all_routes = [route for route in main.app.routes if hasattr(route, 'path')]
        print(f"[SUCCESS] Found {len(all_routes)} total routes")

        print("\n[SUCCESS] Backend structure validation PASSED!")
        print("[SUCCESS] All imports working correctly")
        print("[SUCCESS] Application ready to run")

        return True

    except Exception as e:
        print(f"[ERROR] Backend structure validation FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_project_structure():
    """Display the project structure."""
    print("\n[STRUCTURE] Project structure:")
    current_dir = Path(__file__).parent  # This is the backend directory

    def print_tree(path, prefix="", max_depth=3, current_depth=0):
        if current_depth > max_depth:
            return

        items = []
        for item in path.iterdir():
            if item.name.startswith('.'):
                continue
            items.append(item)

        items.sort(key=lambda x: (x.is_file(), x.name.lower()))

        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "+-- " if is_last else "+-- "  # Use ASCII characters only

            if item.is_dir():
                print(f"{prefix}{current_prefix}{item.name}/")
                extension = "    " if is_last else "    "  # Use spaces only
                print_tree(item, prefix + extension, max_depth, current_depth + 1)
            else:
                print(f"{prefix}{current_prefix}{item.name}")

    print_tree(current_dir)

if __name__ == "__main__":
    print("Backend Structure Validation Tool")
    print("=" * 50)

    success = validate_backend_structure()
    show_project_structure()

    if success:
        print("\nVALIDATION SUCCESSFUL!")
        print("\nTo run the application:")
        print("   cd backend")
        print("   uvicorn main:app --reload")
        print("")
        print("   Or from project root:")
        print("   cd ..")
        print("   PYTHONPATH=./backend uvicorn backend.main:app --reload")
    else:
        print("\nVALIDATION FAILED!")
        sys.exit(1)