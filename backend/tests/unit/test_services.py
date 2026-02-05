"""
Unit tests for service layer
Tests the business logic in service classes
"""
import pytest
from sqlmodel import create_engine, Session, SQLModel
from unittest.mock import Mock, patch
from app.services.task_service import TaskService
from app.models.task import Task, TaskCreate, TaskUpdate
from app.models.user import User
from app.core.exceptions import TaskNotFoundException, UnauthorizedAccessException
from datetime import datetime
import uuid


@pytest.fixture(scope="function")
def mock_session():
    """Create a mock database session"""
    session = Mock(spec=Session)
    return session


def test_create_task_success(mock_session):
    """Test successful task creation"""
    # Arrange
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False
    )
    owner_id = "user123"

    # Act
    with patch('app.models.task.Task') as mock_task_class:
        mock_task_instance = Mock(spec=Task)
        mock_task_instance.id = uuid.uuid4()
        mock_task_instance.title = "Test Task"
        mock_task_instance.description = "Test Description"
        mock_task_instance.completed = False
        mock_task_instance.owner_id = "user123"
        mock_task_instance.created_at = datetime.now()
        mock_task_instance.updated_at = datetime.now()

        mock_task_class.return_value = mock_task_instance

        result = TaskService.create_task(mock_session, task_data, owner_id)

        # Assert
        assert result == mock_task_instance
        mock_session.add.assert_called_once_with(mock_task_instance)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(mock_task_instance)


def test_get_task_by_id_success(mock_session):
    """Test successful task retrieval by ID"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"

    mock_task = Mock(spec=Task)
    mock_task.id = task_id
    mock_task.owner_id = owner_id

    mock_session.get.return_value = mock_task

    # Act
    result = TaskService.get_task_by_id(mock_session, task_id, owner_id)

    # Assert
    assert result == mock_task
    mock_session.get.assert_called_once_with(Task, task_id)


def test_get_task_by_id_not_found(mock_session):
    """Test getting a task that doesn't exist"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"

    mock_session.get.return_value = None

    # Act & Assert
    with pytest.raises(TaskNotFoundException):
        TaskService.get_task_by_id(mock_session, task_id, owner_id)


def test_get_task_by_id_unauthorized(mock_session):
    """Test getting a task owned by a different user"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"
    different_owner_id = "user456"

    mock_task = Mock(spec=Task)
    mock_task.id = task_id
    mock_task.owner_id = different_owner_id

    mock_session.get.return_value = mock_task

    # Act & Assert
    with pytest.raises(UnauthorizedAccessException):
        TaskService.get_task_by_id(mock_session, task_id, owner_id)


def test_get_tasks_by_user_success(mock_session):
    """Test getting all tasks for a user"""
    # Arrange
    owner_id = "user123"

    mock_task1 = Mock(spec=Task)
    mock_task1.id = uuid.uuid4()
    mock_task1.owner_id = owner_id

    mock_task2 = Mock(spec=Task)
    mock_task2.id = uuid.uuid4()
    mock_task2.owner_id = owner_id

    # Mock the exec method to return different results for different queries
    def mock_exec(query):
        if 'count' in str(query).lower():
            # For the count query
            mock_result = Mock()
            mock_result.all.return_value = [mock_task1, mock_task2, Mock(), Mock()]  # 4 items for count
            return mock_result
        else:
            # For the main query
            mock_result = Mock()
            mock_result.all.return_value = [mock_task1, mock_task2]
            return mock_result

    mock_session.exec = mock_exec

    # Act
    tasks, total = TaskService.get_tasks_by_user(mock_session, owner_id)

    # Assert
    assert len(tasks) == 2
    assert total == 4  # This comes from the count query


def test_get_tasks_by_user_with_filters(mock_session):
    """Test getting tasks with completion filter"""
    # Arrange
    owner_id = "user123"
    completed_filter = True

    mock_task = Mock(spec=Task)
    mock_task.id = uuid.uuid4()
    mock_task.owner_id = owner_id
    mock_task.completed = True

    def mock_exec(query):
        if 'count' in str(query).lower():
            # For the count query
            mock_result = Mock()
            mock_result.all.return_value = [mock_task]  # 1 item for count
            return mock_result
        else:
            # For the main query
            mock_result = Mock()
            mock_result.all.return_value = [mock_task]
            return mock_result

    mock_session.exec = mock_exec

    # Act
    tasks, total = TaskService.get_tasks_by_user(mock_session, owner_id, completed=completed_filter)

    # Assert
    assert len(tasks) == 1
    assert total == 1


def test_update_task_success(mock_session):
    """Test successful task update"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"

    mock_existing_task = Mock(spec=Task)
    mock_existing_task.id = task_id
    mock_existing_task.owner_id = owner_id
    mock_existing_task.title = "Old Title"
    mock_existing_task.description = "Old Description"
    mock_existing_task.completed = False
    mock_existing_task.updated_at = datetime.now()

    mock_session.get.return_value = mock_existing_task

    update_data = TaskUpdate(
        title="New Title",
        completed=True
    )

    # Act
    result = TaskService.update_task(mock_session, task_id, update_data, owner_id)

    # Assert
    assert result == mock_existing_task
    assert mock_existing_task.title == "New Title"
    assert mock_existing_task.completed is True
    mock_session.add.assert_called_once_with(mock_existing_task)
    mock_session.commit.assert_called_once()


def test_update_task_not_found(mock_session):
    """Test updating a task that doesn't exist"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"

    mock_session.get.return_value = None

    update_data = TaskUpdate(title="New Title")

    # Act & Assert
    with pytest.raises(TaskNotFoundException):
        TaskService.update_task(mock_session, task_id, update_data, owner_id)


def test_update_task_unauthorized(mock_session):
    """Test updating a task owned by a different user"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"
    different_owner_id = "user456"

    mock_task = Mock(spec=Task)
    mock_task.id = task_id
    mock_task.owner_id = different_owner_id

    mock_session.get.return_value = mock_task

    update_data = TaskUpdate(title="New Title")

    # Act & Assert
    with pytest.raises(UnauthorizedAccessException):
        TaskService.update_task(mock_session, task_id, update_data, owner_id)


def test_delete_task_success(mock_session):
    """Test successful task deletion"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"

    mock_task = Mock(spec=Task)
    mock_task.id = task_id
    mock_task.owner_id = owner_id

    mock_session.get.return_value = mock_task

    # Act
    result = TaskService.delete_task(mock_session, task_id, owner_id)

    # Assert
    assert result is True
    mock_session.delete.assert_called_once_with(mock_task)
    mock_session.commit.assert_called_once()


def test_delete_task_not_found(mock_session):
    """Test deleting a task that doesn't exist"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"

    mock_session.get.return_value = None

    # Act & Assert
    with pytest.raises(TaskNotFoundException):
        TaskService.delete_task(mock_session, task_id, owner_id)


def test_delete_task_unauthorized(mock_session):
    """Test deleting a task owned by a different user"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"
    different_owner_id = "user456"

    mock_task = Mock(spec=Task)
    mock_task.id = task_id
    mock_task.owner_id = different_owner_id

    mock_session.get.return_value = mock_task

    # Act & Assert
    with pytest.raises(UnauthorizedAccessException):
        TaskService.delete_task(mock_session, task_id, owner_id)


def test_toggle_task_completion_success(mock_session):
    """Test successful task completion toggle"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"
    new_completed_status = True

    mock_task = Mock(spec=Task)
    mock_task.id = task_id
    mock_task.owner_id = owner_id
    mock_task.completed = False  # Start as incomplete

    mock_session.get.return_value = mock_task

    # Act
    result = TaskService.toggle_task_completion(mock_session, task_id, new_completed_status, owner_id)

    # Assert
    assert result == mock_task
    assert mock_task.completed == new_completed_status
    mock_session.add.assert_called_once_with(mock_task)
    mock_session.commit.assert_called_once()


def test_toggle_task_completion_not_found(mock_session):
    """Test toggling completion for a task that doesn't exist"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"
    new_completed_status = True

    mock_session.get.return_value = None

    # Act & Assert
    with pytest.raises(TaskNotFoundException):
        TaskService.toggle_task_completion(mock_session, task_id, new_completed_status, owner_id)


def test_toggle_task_completion_unauthorized(mock_session):
    """Test toggling completion for a task owned by a different user"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"
    different_owner_id = "user456"
    new_completed_status = True

    mock_task = Mock(spec=Task)
    mock_task.id = task_id
    mock_task.owner_id = different_owner_id

    mock_session.get.return_value = mock_task

    # Act & Assert
    with pytest.raises(UnauthorizedAccessException):
        TaskService.toggle_task_completion(mock_session, task_id, new_completed_status, owner_id)


def test_update_task_partial_updates(mock_session):
    """Test that only specified fields are updated in partial updates"""
    # Arrange
    task_id = str(uuid.uuid4())
    owner_id = "user123"

    mock_existing_task = Mock(spec=Task)
    mock_existing_task.id = task_id
    mock_existing_task.owner_id = owner_id
    mock_existing_task.title = "Old Title"
    mock_existing_task.description = "Old Description"
    mock_existing_task.completed = False
    mock_existing_task.updated_at = datetime.now()

    mock_session.get.return_value = mock_existing_task

    # Only update the title, leave others unchanged
    update_data = TaskUpdate(title="New Title")

    # Act
    result = TaskService.update_task(mock_session, task_id, update_data, owner_id)

    # Assert
    assert result == mock_existing_task
    assert mock_existing_task.title == "New Title"  # Changed
    assert mock_existing_task.description == "Old Description"  # Unchanged
    assert mock_existing_task.completed is False  # Unchanged
    mock_session.add.assert_called_once_with(mock_existing_task)


if __name__ == "__main__":
    pytest.main([__file__])