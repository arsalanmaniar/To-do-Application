import sys
import os

# Add the project root to the Python path so we can import backend
project_root = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, project_root)

try:
    # Change to the backend directory to run the app
    original_cwd = os.getcwd()
    os.chdir(backend_path)

    # Now import the app from the backend package
    from backend import main
    app = main.app
    print("SUCCESS: Backend app imported successfully!")
    print(f"App title: {app.title}")
    print(f"App description: {app.description}")

    # Check if the auth routes are included
    auth_routes = [route for route in app.routes if '/auth' in route.path]
    print(f"Found {len(auth_routes)} auth routes")

    print("\nBackend structure validation passed!")
    print("All imports working correctly")
    print("Application is ready to run with: uvicorn backend.main:app --reload")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Restore original directory
    os.chdir(original_cwd)