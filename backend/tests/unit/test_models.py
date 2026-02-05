"""
Unit tests for the backend models
"""
import pytest
from app.models.task import Task, TaskCreate
from app.models.user import User, UserBase
from datetime import datetime
import uuid


def test_task_creation():
    """Test creating a task model"""
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False
    )

    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        owner_id="user123"
    )

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False
    assert task.owner_id == "user123"
    assert isinstance(task.id, uuid.UUID)
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_user_creation():
    """Test creating a user model"""
    user = User(
        id="user123",
        email="test@example.com"
    )

    assert user.id == "user123"
    assert user.email == "test@example.com"
    assert isinstance(user.created_at, datetime)


def test_task_update():
    """Test updating task fields"""
    task = Task(
        title="Original Title",
        description="Original Description",
        completed=False,
        owner_id="user123"
    )

    # Update task fields
    task.title = "Updated Title"
    task.description = "Updated Description"
    task.completed = True

    assert task.title == "Updated Title"
    assert task.description == "Updated Description"
    assert task.completed is True