"""
Contract test for task CRUD endpoints
Tests the API contract defined in specs/001-backend-api-todo/contracts/task-api-contract.md
"""
import pytest
import asyncio
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch
from app.main import app
from app.models.task import Task
from app.models.user import User
from datetime import datetime
import uuid


@pytest.mark.asyncio
async def test_task_crud_contract():
    """Test that the task CRUD endpoints follow the defined contract"""
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # Mock the database session and authentication
        with patch('app.core.dependencies.get_db_session') as mock_get_db_session, \
             patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:

            # Mock user ID from JWT
            mock_get_current_user.return_value = "user123"

            # Mock database session
            mock_session = AsyncMock()
            mock_get_db_session.return_value = mock_session

            # Test POST /api/v1/{user_id}/tasks contract
            task_data = {
                "title": "Test Task",
                "description": "Test Description",
                "completed": False
            }

            # Mock the TaskService.create_task to return a task
            with patch('app.services.task_service.TaskService.create_task') as mock_create_task:
                mock_task = Task(
                    id=uuid.uuid4(),
                    title="Test Task",
                    description="Test Description",
                    completed=False,
                    owner_id="user123",
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                mock_create_task.return_value = mock_task

                response = await ac.post("/api/v1/user123/tasks", json=task_data)

                # Verify response follows contract
                assert response.status_code == 201
                response_data = response.json()
                assert "id" in response_data
                assert response_data["title"] == "Test Task"
                assert response_data["description"] == "Test Description"
                assert response_data["completed"] is False
                assert response_data["owner_id"] == "user123"
                assert "created_at" in response_data
                assert "updated_at" in response_data

            # Test GET /api/v1/{user_id}/tasks contract
            with patch('app.services.task_service.TaskService.get_tasks_by_user') as mock_get_tasks:
                mock_get_tasks.return_value = ([mock_task], 1)  # (tasks_list, total_count)

                response = await ac.get("/api/v1/user123/tasks")

                # Verify response follows contract
                assert response.status_code == 200
                response_data = response.json()
                assert "tasks" in response_data
                assert "total" in response_data
                assert "limit" in response_data
                assert "offset" in response_data
                assert len(response_data["tasks"]) == 1
                assert response_data["total"] == 1

                task = response_data["tasks"][0]
                assert "id" in task
                assert task["title"] == "Test Task"
                assert task["description"] == "Test Description"
                assert task["completed"] is False
                assert task["owner_id"] == "user123"
                assert "created_at" in task
                assert "updated_at" in task

            # Test GET /api/v1/{user_id}/tasks/{task_id} contract
            with patch('app.services.task_service.TaskService.get_task_by_id') as mock_get_task:
                mock_get_task.return_value = mock_task

                response = await ac.get(f"/api/v1/user123/tasks/{mock_task.id}")

                # Verify response follows contract
                assert response.status_code == 200
                response_data = response.json()
                assert response_data["id"] == str(mock_task.id)
                assert response_data["title"] == "Test Task"
                assert response_data["description"] == "Test Description"
                assert response_data["completed"] is False
                assert response_data["owner_id"] == "user123"
                assert "created_at" in response_data
                assert "updated_at" in response_data

            # Test PUT /api/v1/{user_id}/tasks/{task_id} contract
            update_data = {
                "title": "Updated Task",
                "description": "Updated Description",
                "completed": True
            }

            updated_mock_task = Task(
                id=mock_task.id,
                title="Updated Task",
                description="Updated Description",
                completed=True,
                owner_id="user123",
                created_at=mock_task.created_at,
                updated_at=datetime.now()
            )

            with patch('app.services.task_service.TaskService.update_task') as mock_update_task:
                mock_update_task.return_value = updated_mock_task

                response = await ac.put(f"/api/v1/user123/tasks/{mock_task.id}", json=update_data)

                # Verify response follows contract
                assert response.status_code == 200
                response_data = response.json()
                assert response_data["id"] == str(updated_mock_task.id)
                assert response_data["title"] == "Updated Task"
                assert response_data["description"] == "Updated Description"
                assert response_data["completed"] is True
                assert response_data["owner_id"] == "user123"
                assert "created_at" in response_data
                assert "updated_at" in response_data

            # Test PATCH /api/v1/{user_id}/tasks/{task_id} contract
            patch_data = {
                "title": "Partially Updated Task"
            }

            patched_mock_task = Task(
                id=mock_task.id,
                title="Partially Updated Task",
                description="Updated Description",
                completed=True,
                owner_id="user123",
                created_at=mock_task.created_at,
                updated_at=datetime.now()
            )

            with patch('app.services.task_service.TaskService.update_task') as mock_patch_task:
                mock_patch_task.return_value = patched_mock_task

                response = await ac.patch(f"/api/v1/user123/tasks/{mock_task.id}", json=patch_data)

                # Verify response follows contract
                assert response.status_code == 200
                response_data = response.json()
                assert response_data["id"] == str(patched_mock_task.id)
                assert response_data["title"] == "Partially Updated Task"

            # Test PATCH /api/v1/{user_id}/tasks/{task_id}/complete contract
            completion_data = {
                "completed": False
            }

            completed_mock_task = Task(
                id=mock_task.id,
                title="Partially Updated Task",
                description="Updated Description",
                completed=False,
                owner_id="user123",
                created_at=mock_task.created_at,
                updated_at=datetime.now()
            )

            with patch('app.services.task_service.TaskService.toggle_task_completion') as mock_toggle_completion:
                mock_toggle_completion.return_value = completed_mock_task

                response = await ac.patch(f"/api/v1/user123/tasks/{mock_task.id}/complete", json=completion_data)

                # Verify response follows contract
                assert response.status_code == 200
                response_data = response.json()
                assert response_data["id"] == str(completed_mock_task.id)
                assert response_data["completed"] is False

            # Test DELETE /api/v1/{user_id}/tasks/{task_id} contract
            with patch('app.services.task_service.TaskService.delete_task') as mock_delete_task:
                mock_delete_task.return_value = True

                response = await ac.delete(f"/api/v1/user123/tasks/{mock_task.id}")

                # Verify response follows contract
                assert response.status_code == 204


@pytest.mark.asyncio
async def test_authentication_contract():
    """Test that authentication contract is properly enforced"""
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # Test that endpoints require authentication
        with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
            mock_get_current_user.side_effect = Exception("Unauthorized")

            response = await ac.get("/api/v1/user123/tasks")

            # Should return 401 or 403 depending on implementation
            assert response.status_code in [401, 403]


@pytest.mark.asyncio
async def test_error_response_contract():
    """Test that error responses follow the contract"""
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # Test error responses with proper status codes
        with patch('app.core.dependencies.get_current_user_id_matching_path') as mock_get_current_user:
            mock_get_current_user.return_value = "user123"

            # Test invalid request data (should return 400)
            invalid_task_data = {
                "title": "",  # Invalid - empty title
                "description": "Valid description"
            }

            response = await ac.post("/api/v1/user123/tasks", json=invalid_task_data)

            # Should return 400 for validation errors
            assert response.status_code == 422  # Pydantic validation error


if __name__ == "__main__":
    pytest.main([__file__])