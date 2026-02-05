"""
Integration test for task management flow
Tests the complete task management workflow including authentication, database operations, and API endpoints
"""
import pytest
import os
from sqlmodel import create_engine, Session, SQLModel
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import get_session
from app.models.task import Task, TaskCreate
from app.models.user import User
from app.core.security import create_access_token
from datetime import datetime
import uuid


@pytest.fixture(scope="function")
def test_client_and_db():
    """Create a test client with an in-memory database"""
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})

    # Create all tables
    SQLModel.metadata.create_all(bind=engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    # Override the session dependency
    app.dependency_overrides[get_session] = get_test_session

    with TestClient(app) as client:
        yield client, engine

    # Clean up
    app.dependency_overrides.clear()


def test_task_management_flow(test_client_and_db):
    """Test the complete task management flow"""
    client, engine = test_client_and_db

    # Create a test user in the database
    with Session(engine) as session:
        user = User(id="test_user_123", email="test@example.com")
        session.add(user)
        session.commit()

        # Verify user was created
        assert session.get(User, "test_user_123") is not None

    # Mock JWT token for authentication
    fake_jwt_token = "fake.jwt.token"

    with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
        mock_get_current_user.return_value = "test_user_123"

        # Test 1: Create a task
        task_data = {
            "title": "Integration Test Task",
            "description": "This is a test task for integration testing",
            "completed": False
        }

        response = client.post(
            f"/api/v1/test_user_123/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {fake_jwt_token}"}
        )

        assert response.status_code == 201
        created_task = response.json()
        assert created_task["title"] == "Integration Test Task"
        assert created_task["description"] == "This is a test task for integration testing"
        assert created_task["completed"] is False
        assert created_task["owner_id"] == "test_user_123"
        assert "id" in created_task

        task_id = created_task["id"]

        # Test 2: Get the created task
        response = client.get(
            f"/api/v1/test_user_123/tasks/{task_id}",
            headers={"Authorization": f"Bearer {fake_jwt_token}"}
        )

        assert response.status_code == 200
        retrieved_task = response.json()
        assert retrieved_task["id"] == task_id
        assert retrieved_task["title"] == "Integration Test Task"

        # Test 3: Get all tasks for the user
        response = client.get(
            f"/api/v1/test_user_123/tasks",
            headers={"Authorization": f"Bearer {fake_jwt_token}"}
        )

        assert response.status_code == 200
        task_list = response.json()
        assert task_list["total"] >= 1
        assert len(task_list["tasks"]) >= 1
        assert any(task["id"] == task_id for task in task_list["tasks"])

        # Test 4: Update the task
        update_data = {
            "title": "Updated Integration Test Task",
            "description": "Updated description",
            "completed": True
        }

        response = client.put(
            f"/api/v1/test_user_123/tasks/{task_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {fake_jwt_token}"}
        )

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["id"] == task_id
        assert updated_task["title"] == "Updated Integration Test Task"
        assert updated_task["completed"] is True

        # Test 5: Partially update the task (PATCH)
        patch_data = {
            "title": "Patched Integration Test Task"
        }

        response = client.patch(
            f"/api/v1/test_user_123/tasks/{task_id}",
            json=patch_data,
            headers={"Authorization": f"Bearer {fake_jwt_token}"}
        )

        assert response.status_code == 200
        patched_task = response.json()
        assert patched_task["id"] == task_id
        assert patched_task["title"] == "Patched Integration Test Task"
        # Completed status should remain True
        assert patched_task["completed"] is True

        # Test 6: Toggle task completion status
        completion_data = {
            "completed": False
        }

        response = client.patch(
            f"/api/v1/test_user_123/tasks/{task_id}/complete",
            json=completion_data,
            headers={"Authorization": f"Bearer {fake_jwt_token}"}
        )

        assert response.status_code == 200
        toggled_task = response.json()
        assert toggled_task["id"] == task_id
        assert toggled_task["completed"] is False

        # Test 7: Delete the task
        response = client.delete(
            f"/api/v1/test_user_123/tasks/{task_id}",
            headers={"Authorization": f"Bearer {fake_jwt_token}"}
        )

        assert response.status_code == 204

        # Verify the task was deleted
        response = client.get(
            f"/api/v1/test_user_123/tasks/{task_id}",
            headers={"Authorization": f"Bearer {fake_jwt_token}"}
        )

        assert response.status_code == 404


def test_cross_user_isolation(test_client_and_db):
    """Test that users cannot access each other's tasks"""
    client, engine = test_client_and_db

    # Create two test users in the database
    with Session(engine) as session:
        user1 = User(id="user1", email="user1@example.com")
        user2 = User(id="user2", email="user2@example.com")
        session.add(user1)
        session.add(user2)
        session.commit()

    # Mock JWT tokens for different users
    with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
        # First, create a task as user1
        mock_get_current_user.return_value = "user1"

        task_data = {
            "title": "User1's Task",
            "description": "This belongs to user1",
            "completed": False
        }

        response = client.post(
            f"/api/v1/user1/tasks",
            json=task_data,
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 201
        user1_task = response.json()
        task_id = user1_task["id"]
        assert user1_task["owner_id"] == "user1"

    # Now try to access that task as user2 (should fail)
    with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
        mock_get_current_user.return_value = "user2"

        response = client.get(
            f"/api/v1/user2/tasks/{task_id}",
            headers={"Authorization": "Bearer fake_token"}
        )

        # Should return 404 because user2 doesn't own this task
        assert response.status_code == 404

    # Also test that user2 can't access user1's task even with user1's ID in URL
    with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
        mock_get_current_user.return_value = "user2"

        response = client.get(
            f"/api/v1/user1/tasks/{task_id}",
            headers={"Authorization": "Bearer fake_token"}
        )

        # Should return 403 because JWT user doesn't match URL user
        assert response.status_code in [403, 404]


def test_task_validation(test_client_and_db):
    """Test that task validation works correctly"""
    client, engine = test_client_and_db

    # Create a test user
    with Session(engine) as session:
        user = User(id="validator_user", email="validator@example.com")
        session.add(user)
        session.commit()

    with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
        mock_get_current_user.return_value = "validator_user"

        # Test creating a task with invalid title (too short)
        invalid_task_data = {
            "title": "",  # Empty title should fail validation
            "description": "Valid description",
            "completed": False
        }

        response = client.post(
            f"/api/v1/validator_user/tasks",
            json=invalid_task_data,
            headers={"Authorization": "Bearer fake_token"}
        )

        # Should return 422 for validation error
        assert response.status_code == 422

        # Test creating a task with invalid title (too long)
        invalid_task_data = {
            "title": "x" * 256,  # Too long title should fail validation
            "description": "Valid description",
            "completed": False
        }

        response = client.post(
            f"/api/v1/validator_user/tasks",
            json=invalid_task_data,
            headers={"Authorization": "Bearer fake_token"}
        )

        # Should return 422 for validation error
        assert response.status_code == 422

        # Test creating a task with valid data
        valid_task_data = {
            "title": "Valid Task Title",
            "description": "x" * 2000,  # Maximum length description
            "completed": False
        }

        response = client.post(
            f"/api/v1/validator_user/tasks",
            json=valid_task_data,
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 201
        created_task = response.json()
        assert created_task["title"] == "Valid Task Title"


if __name__ == "__main__":
    pytest.main([__file__])