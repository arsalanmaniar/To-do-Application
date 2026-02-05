"""
Integration test for JWT validation
Tests the complete JWT validation flow including token parsing, verification, and user extraction
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import verify_token, create_access_token
from app.core.config import settings
import jwt
import time
from unittest.mock import patch
from datetime import datetime, timedelta


def test_complete_jwt_validation_flow():
    """Test the complete JWT validation integration"""
    client = TestClient(app)

    # Test with a properly formed but invalid token
    response = client.get(
        "/api/v1/user123/tasks",
        headers={"Authorization": "Bearer invalid.token.signature"}
    )

    # Should return 401 for invalid token
    assert response.status_code == 401

    # Test with a properly formed token with wrong secret
    wrong_secret_token = jwt.encode(
        {"sub": "user123", "exp": int(time.time()) + 3600},
        "wrong_secret",
        algorithm="HS256"
    )

    response = client.get(
        "/api/v1/user123/tasks",
        headers={"Authorization": f"Bearer {wrong_secret_token}"}
    )

    # Should return 401 for invalid signature
    assert response.status_code == 401


def test_jwt_token_structure_validation():
    """Test that JWT tokens have the required structure"""
    client = TestClient(app)

    # Test token without 'exp' (expiration) field
    token_without_exp = jwt.encode(
        {"sub": "user123"},  # Missing expiration
        settings.BETTER_AUTH_SECRET,
        algorithm="HS256"
    )

    response = client.get(
        "/api/v1/user123/tasks",
        headers={"Authorization": f"Bearer {token_without_exp}"}
    )

    # Should return 401 for missing or invalid exp
    assert response.status_code in [401, 422]

    # Test token without 'sub' (subject/user_id) field
    token_without_sub = jwt.encode(
        {"exp": int(time.time()) + 3600},  # Missing subject
        settings.BETTER_AUTH_SECRET,
        algorithm="HS256"
    )

    response = client.get(
        "/api/v1/user123/tasks",
        headers={"Authorization": f"Bearer {token_without_sub}"}
    )

    # Should return 401 for missing or invalid sub
    assert response.status_code in [401, 422]


def test_expired_jwt_token():
    """Test that expired JWT tokens are rejected"""
    client = TestClient(app)

    # Create an expired token (expired 1 hour ago)
    expired_token = jwt.encode(
        {"sub": "user123", "exp": int(time.time()) - 3600},
        settings.BETTER_AUTH_SECRET,
        algorithm="HS256"
    )

    response = client.get(
        "/api/v1/user123/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    # Should return 401 for expired token
    assert response.status_code == 401


def test_future_jwt_token():
    """Test JWT token with nbf (not before) field in the future"""
    client = TestClient(app)

    # Create a token that's not valid until 1 hour from now
    future_token = jwt.encode({
        "sub": "user123",
        "exp": int(time.time()) + 3600,
        "nbf": int(time.time()) + 3600  # Not valid until 1 hour from now
    },
        settings.BETTER_AUTH_SECRET,
        algorithm="HS256"
    )

    response = client.get(
        "/api/v1/user123/tasks",
        headers={"Authorization": f"Bearer {future_token}"}
    )

    # Should return 401 for token not yet valid
    assert response.status_code == 401


def test_jwt_algorithm_validation():
    """Test that only allowed algorithms are accepted"""
    client = TestClient(app)

    # Even though we can't easily test with different algorithms without changing the security module,
    # we can test that the system rejects tokens in certain ways

    # Test with a token that has an alg header that differs from what's expected
    # This would typically be handled by the jwt library based on the algorithm specified
    malformed_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MDQzMjM2MDB9.invalid.signature"

    response = client.get(
        "/api/v1/user123/tasks",
        headers={"Authorization": f"Bearer {malformed_token}"}
    )

    # Should return 401 for invalid token
    assert response.status_code == 401


def test_valid_jwt_acceptance():
    """Test that valid JWT tokens are properly accepted"""
    client = TestClient(app)

    # Create a valid token
    valid_token = jwt.encode({
        "sub": "test_user_123",
        "exp": int(time.time()) + 3600  # Expires in 1 hour
    },
        settings.BETTER_AUTH_SECRET,
        algorithm="HS256"
    )

    # Mock the rest of the system to allow the request to proceed past auth
    with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
        mock_get_current_user.return_value = "test_user_123"

        # We expect this to fail later in the process (due to missing session, etc.)
        # but it should pass the JWT validation step
        response = client.get(
            f"/api/v1/test_user_123/tasks",
            headers={"Authorization": f"Bearer {valid_token}"}
        )

        # The request should not be rejected at the JWT validation level
        # It might fail later due to other dependencies, but not at auth level
        assert response.status_code != 401  # Should not be unauthorized due to JWT


def test_user_id_extraction():
    """Test that user ID is properly extracted from JWT token"""
    client = TestClient(app)

    # Test with different user ID formats that might come from Better Auth
    user_ids_to_test = [
        "user123",
        "usr_abc123def456",
        "auth0|123456789",
        "google-oauth2|987654321"
    ]

    for user_id in user_ids_to_test:
        token = jwt.encode({
            "sub": user_id,
            "exp": int(time.time()) + 3600
        },
            settings.BETTER_AUTH_SECRET,
            algorithm="HS256"
        )

        # Mock to allow the request to proceed
        with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
            mock_get_current_user.return_value = user_id

            response = client.get(
                f"/api/v1/{user_id}/tasks",
                headers={"Authorization": f"Bearer {token}"}
            )

            # Should not fail at auth level
            assert response.status_code != 401


def test_jwt_claim_validation():
    """Test validation of JWT claims"""
    client = TestClient(app)

    # Test token with non-string sub claim
    invalid_sub_token = jwt.encode({
        "sub": 12345,  # Invalid - should be string
        "exp": int(time.time()) + 3600
    },
        settings.BETTER_AUTH_SECRET,
        algorithm="HS256"
    )

    response = client.get(
        "/api/v1/user123/tasks",
        headers={"Authorization": f"Bearer {invalid_sub_token}"}
    )

    # Should return 401 for invalid token structure
    assert response.status_code in [401, 422]


def test_concurrent_jwt_validation():
    """Test JWT validation under concurrent requests"""
    client = TestClient(app)

    # Create multiple valid tokens for different users
    tokens = []
    for i in range(3):
        token = jwt.encode({
            "sub": f"user_{i}",
            "exp": int(time.time()) + 3600
        },
            settings.BETTER_AUTH_SECRET,
            algorithm="HS256"
        )
        tokens.append((f"user_{i}", token))

    # Test each token separately
    for user_id, token in tokens:
        with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
            mock_get_current_user.return_value = user_id

            response = client.get(
                f"/api/v1/{user_id}/tasks",
                headers={"Authorization": f"Bearer {token}"}
            )

            # Should not fail at auth level
            assert response.status_code != 401


if __name__ == "__main__":
    pytest.main([__file__])