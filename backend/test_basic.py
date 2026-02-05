"""
Basic integration test to verify the API is working
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


def test_health_endpoint():
    """Test the health check endpoint"""
    client = TestClient(app)

    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


if __name__ == "__main__":
    test_health_endpoint()
    print("Health check test passed!")