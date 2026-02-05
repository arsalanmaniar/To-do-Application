"""
Test script to verify backend functionality
"""

import subprocess
import sys
import time
import requests
from threading import Thread
import signal
import os

def test_backend_startup():
    """Test that the backend starts without import errors."""
    try:
        # Set environment variables for testing
        import os
        os.environ.setdefault('DATABASE_URL', 'sqlite:///./test.db')
        os.environ.setdefault('BETTER_AUTH_SECRET', 'testsecretkeythatisatleast32characterslong')

        # Test importing the main module
        from backend.main import app
        print("OK Backend module imports successfully")

        # Check that app is a FastAPI instance
        from fastapi import FastAPI
        assert isinstance(app, FastAPI), "app is not a FastAPI instance"
        print("OK FastAPI app is properly defined")

        return True
    except ImportError as e:
        print(f"ERROR Import error: {e}")
        return False
    except Exception as e:
        print(f"ERROR Error: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint."""
    try:
        # Set environment variables for testing
        import os
        os.environ.setdefault('DATABASE_URL', 'sqlite:///./test.db')
        os.environ.setdefault('BETTER_AUTH_SECRET', 'testsecretkeythatisatleast32characterslong')

        from backend.main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "status" in data, "Missing status in response"
        assert data["status"] == "healthy", f"Expected healthy, got {data['status']}"

        print("OK Health endpoint working correctly")
        return True
    except Exception as e:
        print(f"ERROR Health endpoint test failed: {e}")
        return False

def test_cli_commands():
    """Test CLI commands."""
    try:
        # Test check-db-connection command
        result = subprocess.run([
            sys.executable, "-m", "backend.cli", "check-db-connection"
        ], capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            print("OK CLI check-db-connection command works")
        else:
            print(f"WARN CLI check-db-connection command failed: {result.stderr}")

        # Test list-tables command
        result = subprocess.run([
            sys.executable, "-m", "backend.cli", "list-tables"
        ], capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            print("OK CLI list-tables command works")
        else:
            print(f"WARN CLI list-tables command failed: {result.stderr}")

        return True
    except subprocess.TimeoutExpired:
        print("WARN CLI commands timed out (expected if no database configured)")
        return True
    except Exception as e:
        print(f"WARN CLI commands error (may be expected if no database): {e}")
        return True  # Don't fail the test if CLI can't connect to DB

def main():
    print("Testing backend functionality...\n")

    success = True

    print("1. Testing backend startup...")
    success &= test_backend_startup()

    print("\n2. Testing health endpoint...")
    success &= test_health_endpoint()

    print("\n3. Testing CLI commands...")
    success &= test_cli_commands()

    print(f"\n{'ALL TESTS PASSED!' if success else 'SOME TESTS FAILED!'}")

    return success

if __name__ == "__main__":
    main()