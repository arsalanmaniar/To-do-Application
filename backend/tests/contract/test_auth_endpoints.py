"""
Contract test for authentication validation
Tests the authentication contract defined in the API specifications
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
import jwt
from app.core.config import settings


def test_auth_contract():
    """Test that authentication validation follows the contract"""
    client = TestClient(app)

    # Test that endpoints require JWT token in Authorization header
    response = client.get("/api/v1/user123/tasks")

    # Should return 401 for missing authorization
    assert response.status_code in [401, 422]  # Could be 401 Unauthorized or 422 if path params missing

    # Test with malformed Authorization header
    response = client.get(
        "/api/v1/user123/tasks",
        headers={"Authorization": "Invalid Token Format"}
    )

    # Should return 401 for invalid authorization format
    assert response.status_code == 401

    # Test with valid JWT token format but invalid signature
    response = client.get(
        "/api/v1/user123/tasks",
        headers={"Authorization": "Bearer invalid.jwt.token"}
    )

    # Should return 401 for invalid token
    assert response.status_code == 401

    # Test that user_id in URL must match user_id in JWT
    with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
        # Mock a different user ID from JWT than in URL
        mock_get_current_user.return_value = "different_user_from_jwt"

        response = client.get(
            "/api/v1/original_user/tasks",
            headers={"Authorization": "Bearer valid.token.here"}
        )

        # Should return 403 for user ID mismatch
        assert response.status_code == 403


def test_jwt_verification_contract():
    """Test JWT token verification contract"""
    client = TestClient(app)

    # Test with expired token
    with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
        mock_get_current_user.side_effect = jwt.ExpiredSignatureError("Token has expired")

        response = client.get(
            "/api/v1/user123/tasks",
            headers={"Authorization": "Bearer expired.token.here"}
        )

        # Should return 401 for expired token
        assert response.status_code == 401

    # Test with invalid token algorithm
    with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
        mock_get_current_user.side_effect = jwt.InvalidAlgorithmError("Wrong algorithm")

        response = client.get(
            "/api/v1/user123/tasks",
            headers={"Authorization": "Bearer invalid.algo.token"}
        )

        # Should return 401 for invalid algorithm
        assert response.status_code == 401

    # Test with malformed token
    with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
        mock_get_current_user.side_effect = jwt.DecodeError("Malformed token")

        response = client.get(
            "/api/v1/user123/tasks",
            headers={"Authorization": "Bearer malformed.token"}
        )

        # Should return 401 for malformed token
        assert response.status_code == 401


def test_auth_headers_contract():
    """Test that authentication headers follow the contract"""
    client = TestClient(app)

    # Test with Bearer token format (correct)
    with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
        mock_get_current_user.return_value = "user123"

        response = client.get(
            "/api/v1/user123/tasks",
            headers={"Authorization": "Bearer valid.token"}
        )

        # Should proceed with the request (might return 200 or other status depending on other factors)
        assert response.status_code != 401  # Should not be unauthorized at auth level

    # Test with wrong header format
    response = client.get(
        "/api/v1/user123/tasks",
        headers={"X-API-Key": "some-api-key"}
    )

    # Should return 401 for missing proper auth header
    assert response.status_code in [401, 422]


def test_endpoint_auth_enforcement():
    """Test that all endpoints enforce authentication"""
    client = TestClient(app)

    # Test all endpoint methods without authentication
    endpoints_to_test = [
        ("GET", "/api/v1/user123/tasks"),
        ("POST", "/api/v1/user123/tasks"),
        ("GET", "/api/v1/user123/tasks/task123"),
        ("PUT", "/api/v1/user123/tasks/task123"),
        ("PATCH", "/api/v1/user123/tasks/task123"),
        ("PATCH", "/api/v1/user123/tasks/task123/complete"),
        ("DELETE", "/api/v1/user123/tasks/task123"),
    ]

    for method, url in endpoints_to_test:
        if method == "GET":
            response = client.get(url)
        elif method == "POST":
            response = client.post(url, json={})
        elif method == "PUT":
            response = client.put(url, json={})
        elif method == "PATCH":
            response = client.patch(url, json={})
        elif method == "DELETE":
            response = client.delete(url)

        # All should return 401 (unauthorized) or 422 (validation error due to missing auth) when missing auth
        assert response.status_code in [401, 422], f"{method} {url} should require authentication"


def test_user_id_consistency_contract():
    """Test that user ID consistency is enforced across the contract"""
    client = TestClient(app)

    # Test that the user_id in the path matches the user_id extracted from JWT
    with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
        # Scenario: JWT has user2 but URL has user1
        mock_get_current_user.return_value = "user2_from_jwt"

        # Test various endpoints with mismatched user IDs
        endpoints = [
            "/api/v1/user1_from_path/tasks",
            "/api/v1/user1_from_path/tasks/task123",
            "/api/v1/user1_from_path/tasks/task123/complete"
        ]

        for endpoint in endpoints:
            response = client.get(
                endpoint,
                headers={"Authorization": "Bearer token_for_user2"}
            )

            # Should return 403 for user ID mismatch
            assert response.status_code == 403, f"Endpoint {endpoint} should enforce user ID consistency"


if __name__ == "__main__":
    pytest.main([__file__])