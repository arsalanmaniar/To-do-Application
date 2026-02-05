import sys
import os

# Add the project root to Python path so 'backend' package can be found
# Get the directory containing this file (backend directory), then go up one level to project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Now run the uvicorn server
import uvicorn

if __name__ == "__main__":
    print("Starting server...")
    # Use the absolute module path that uvicorn can find
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)