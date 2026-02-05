"""
Integration test for database operations
Tests the complete database interaction flow including connections, transactions, and ORM operations
"""
import pytest
from sqlmodel import create_engine, Session, SQLModel, select
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import get_session
from app.models.task import Task
from app.models.user import User
from app.services.task_service import TaskService
from datetime import datetime
import uuid


@pytest.fixture(scope="function")
def test_db_session():
    """Create a test database session"""
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///test_database.db", connect_args={"check_same_thread": False})

    # Create all tables
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session, engine


def test_database_connection_integration(test_db_session):
    """Test that database connections work properly"""
    session, engine = test_db_session

    # Test basic database operations
    user = User(id="db_conn_test", email="dbtest@example.com")
    session.add(user)
    session.commit()

    # Retrieve the user back
    retrieved_user = session.get(User, "db_conn_test")
    assert retrieved_user is not None
    assert retrieved_user.id == "db_conn_test"
    assert retrieved_user.email == "dbtest@example.com"


def test_task_database_operations_integration(test_db_session):
    """Test complete task database operations"""
    session, engine = test_db_session

    # Create a user
    user = User(id="task_op_user", email="taskop@example.com")
    session.add(user)
    session.commit()

    # Test creating a task via TaskService
    from app.models.task import TaskCreate
    task_data = TaskCreate(
        title="Database Integration Test Task",
        description="Testing database operations",
        completed=False
    )

    created_task = TaskService.create_task(session, task_data, "task_op_user")
    assert created_task.id is not None
    assert created_task.title == "Database Integration Test Task"
    assert created_task.owner_id == "task_op_user"

    # Test retrieving the task via TaskService
    retrieved_task = TaskService.get_task_by_id(session, str(created_task.id), "task_op_user")
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Database Integration Test Task"

    # Test retrieving all tasks for the user
    tasks, total = TaskService.get_tasks_by_user(session, "task_op_user")
    assert len(tasks) == 1
    assert total == 1
    assert tasks[0].id == created_task.id

    # Test updating the task
    from app.models.task import TaskUpdate
    update_data = TaskUpdate(
        title="Updated Database Test Task",
        completed=True
    )

    updated_task = TaskService.update_task(session, str(created_task.id), update_data, "task_op_user")
    assert updated_task.id == created_task.id
    assert updated_task.title == "Updated Database Test Task"
    assert updated_task.completed is True

    # Test toggling completion status
    toggled_task = TaskService.toggle_task_completion(session, str(created_task.id), False, "task_op_user")
    assert toggled_task.id == created_task.id
    assert toggled_task.completed is False

    # Test deleting the task
    result = TaskService.delete_task(session, str(created_task.id), "task_op_user")
    assert result is True

    # Verify the task is gone
    tasks, total = TaskService.get_tasks_by_user(session, "task_op_user")
    assert len(tasks) == 0
    assert total == 0


def test_database_transaction_integration(test_db_session):
    """Test database transaction behavior"""
    session, engine = test_db_session

    # Create a user
    user = User(id="transaction_user", email="transaction@example.com")
    session.add(user)
    session.commit()

    # Test transaction rollback behavior
    from app.models.task import TaskCreate
    original_task_count = len(session.exec(select(Task).where(Task.owner_id == "transaction_user")).all())

    try:
        # Attempt to create a task
        task_data = TaskCreate(title="Transaction Test", description="Will be rolled back", completed=False)
        created_task = TaskService.create_task(session, task_data, "transaction_user")

        # Manually trigger a rollback-like scenario
        session.rollback()  # This should revert the task creation

        # Check that the task was not saved
        final_task_count = len(session.exec(select(Task).where(Task.owner_id == "transaction_user")).all())
        assert final_task_count == original_task_count

    except Exception:
        # If any exception occurred, verify rollback happened
        final_task_count = len(session.exec(select(Task).where(Task.owner_id == "transaction_user")).all())
        assert final_task_count == original_task_count


def test_database_filtering_integration(test_db_session):
    """Test database filtering operations"""
    session, engine = test_db_session

    # Create a user
    user = User(id="filter_user", email="filter@example.com")
    session.add(user)
    session.commit()

    # Create multiple tasks with different completion statuses
    from app.models.task import TaskCreate

    # Create completed tasks
    for i in range(2):
        task_data = TaskCreate(
            title=f"Completed Task {i}",
            description=f"Completed task {i} for filtering",
            completed=True
        )
        TaskService.create_task(session, task_data, "filter_user")

    # Create incomplete tasks
    for i in range(3):
        task_data = TaskCreate(
            title=f"Incomplete Task {i}",
            description=f"Incomplete task {i} for filtering",
            completed=False
        )
        TaskService.create_task(session, task_data, "filter_user")

    # Test filtering by completion status
    completed_tasks, completed_count = TaskService.get_tasks_by_user(session, "filter_user", completed=True)
    assert len(completed_tasks) == 2
    assert completed_count == 2
    for task in completed_tasks:
        assert task.completed is True

    incomplete_tasks, incomplete_count = TaskService.get_tasks_by_user(session, "filter_user", completed=False)
    assert len(incomplete_tasks) == 3
    assert incomplete_count == 3
    for task in incomplete_tasks:
        assert task.completed is False

    # Test getting all tasks
    all_tasks, all_count = TaskService.get_tasks_by_user(session, "filter_user")
    assert len(all_tasks) == 5
    assert all_count == 5


def test_database_pagination_integration(test_db_session):
    """Test database pagination operations"""
    session, engine = test_db_session

    # Create a user
    user = User(id="pagination_user", email="pagination@example.com")
    session.add(user)
    session.commit()

    # Create multiple tasks
    from app.models.task import TaskCreate

    for i in range(10):
        task_data = TaskCreate(
            title=f"Paginated Task {i}",
            description=f"Task {i} for pagination testing",
            completed=(i % 2 == 0)  # Alternate completion status
        )
        TaskService.create_task(session, task_data, "pagination_user")

    # Test pagination
    first_page, total = TaskService.get_tasks_by_user(session, "pagination_user", limit=3, offset=0)
    assert len(first_page) == 3
    assert total == 10

    second_page, total = TaskService.get_tasks_by_user(session, "pagination_user", limit=3, offset=3)
    assert len(second_page) == 3
    assert total == 10

    third_page, total = TaskService.get_tasks_by_user(session, "pagination_user", limit=3, offset=6)
    assert len(third_page) == 3  # Actually 4 left, but limit is 3
    assert total == 10

    fourth_page, total = TaskService.get_tasks_by_user(session, "pagination_user", limit=3, offset=9)
    assert len(fourth_page) == 1  # Last task
    assert total == 10

    # Ensure no overlap between pages
    first_ids = {str(task.id) for task in first_page}
    second_ids = {str(task.id) for task in second_page}
    third_ids = {str(task.id) for task in third_page}
    fourth_ids = {str(task.id) for task in fourth_page}

    # Verify no overlap between pages
    assert len(first_ids.intersection(second_ids)) == 0
    assert len(first_ids.intersection(third_ids)) == 0
    assert len(first_ids.intersection(fourth_ids)) == 0
    assert len(second_ids.intersection(third_ids)) == 0
    assert len(second_ids.intersection(fourth_ids)) == 0
    assert len(third_ids.intersection(fourth_ids)) == 0


def test_database_relationship_integration(test_db_session):
    """Test database relationships"""
    session, engine = test_db_session

    # Create a user
    user = User(id="relationship_user", email="relationship@example.com")
    session.add(user)
    session.commit()

    # Create a task for the user
    from app.models.task import TaskCreate
    task_data = TaskCreate(
        title="Relationship Test Task",
        description="Testing user-task relationship",
        completed=False
    )
    created_task = TaskService.create_task(session, task_data, "relationship_user")

    # Verify the relationship exists by checking foreign key
    assert created_task.owner_id == "relationship_user"

    # Retrieve and verify the relationship
    retrieved_task = session.get(Task, created_task.id)
    assert retrieved_task.owner_id == "relationship_user"

    # Verify the user can retrieve their task
    user_tasks, _ = TaskService.get_tasks_by_user(session, "relationship_user")
    assert len(user_tasks) == 1
    assert user_tasks[0].id == created_task.id


def test_database_data_integrity_integration(test_db_session):
    """Test database data integrity constraints"""
    session, engine = test_db_session

    # Create a user
    user = User(id="integrity_user", email="integrity@example.com")
    session.add(user)
    session.commit()

    # Test with valid data lengths
    from app.models.task import TaskCreate

    # Test maximum title length (255 chars)
    max_title = "x" * 255
    task_data = TaskCreate(title=max_title, description="Valid max length title", completed=False)
    max_title_task = TaskService.create_task(session, task_data, "integrity_user")
    assert max_title_task.title == max_title

    # Test maximum description length (2000 chars)
    max_desc = "y" * 2000
    task_data = TaskCreate(title="Max Description Task", description=max_desc, completed=False)
    max_desc_task = TaskService.create_task(session, task_data, "integrity_user")
    assert max_desc_task.description == max_desc

    # Test minimum title length (1 char)
    min_title_task = TaskService.create_task(
        session, TaskCreate(title="x", description="Min length title", completed=False), "integrity_user"
    )
    assert min_title_task.title == "x"

    # Verify all tasks were created
    all_tasks, total = TaskService.get_tasks_by_user(session, "integrity_user")
    assert len(all_tasks) == 3
    assert total == 3


def test_database_concurrency_simulation(test_db_session):
    """Test database operations that might occur concurrently"""
    session, engine = test_db_session

    # Create a user
    user = User(id="concurrent_user", email="concurrent@example.com")
    session.add(user)
    session.commit()

    # Simulate multiple operations on the same user
    from app.models.task import TaskCreate

    # Create several tasks rapidly
    created_tasks = []
    for i in range(5):
        task_data = TaskCreate(
            title=f"Concurrent Task {i}",
            description=f"Task {i} created in sequence",
            completed=False
        )
        task = TaskService.create_task(session, task_data, "concurrent_user")
        created_tasks.append(task)

    # Verify all were created successfully
    all_tasks, total = TaskService.get_tasks_by_user(session, "concurrent_user")
    assert len(all_tasks) == 5
    assert total == 5

    # Update multiple tasks in sequence
    from app.models.task import TaskUpdate
    for i, task in enumerate(created_tasks):
        update_data = TaskUpdate(title=f"Updated Concurrent Task {i}", completed=True)
        updated_task = TaskService.update_task(session, str(task.id), update_data, "concurrent_user")
        assert updated_task.title == f"Updated Concurrent Task {i}"
        assert updated_task.completed is True

    # Verify all were updated
    updated_tasks, total = TaskService.get_tasks_by_user(session, "concurrent_user")
    assert len(updated_tasks) == 5
    assert total == 5
    for task in updated_tasks:
        assert task.completed is True


if __name__ == "__main__":
    pytest.main([__file__])