from sqlmodel import Session, select
from typing import List, Optional
from app.models.task import Task, TaskCreate, TaskUpdate
from app.core.exceptions import TaskNotFoundException, UnauthorizedAccessException
from app.core.logging import logger


class TaskService:
    """
    Service class for handling task-related operations
    """

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, owner_id: str) -> Task:
        """
        Create a new task for a user
        """
        task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            owner_id=owner_id
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Created task {task.id} for user {owner_id}")
        return task

    @staticmethod
    def get_task_by_id(session: Session, task_id: str, owner_id: str) -> Task:
        """
        Get a specific task by ID for a specific user
        """
        from uuid import UUID
        # Convert string ID to UUID object for proper database query
        uuid_obj = UUID(task_id) if isinstance(task_id, str) and task_id else task_id
        task = session.get(Task, uuid_obj)
        if not task:
            raise TaskNotFoundException(task_id)

        if task.owner_id != owner_id:
            raise UnauthorizedAccessException()

        return task

    @staticmethod
    def get_tasks_by_user(
        session: Session,
        owner_id: str,
        completed: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> tuple[List[Task], int]:
        """
        Get all tasks for a specific user with optional filtering
        """
        query = select(Task).where(Task.owner_id == owner_id)

        if completed is not None:
            query = query.where(Task.completed == completed)

        # Get total count for pagination
        count_query = select(Task).where(Task.owner_id == owner_id)
        if completed is not None:
            count_query = count_query.where(Task.completed == completed)
        total = len(session.exec(count_query).all())

        # Apply pagination
        query = query.offset(offset).limit(limit)
        tasks = session.exec(query).all()

        return tasks, total

    @staticmethod
    def update_task(session: Session, task_id: str, task_data: TaskUpdate, owner_id: str) -> Task:
        """
        Update a specific task for a user
        """
        from uuid import UUID
        # Convert string ID to UUID object for proper database query
        uuid_obj = UUID(task_id) if isinstance(task_id, str) and task_id else task_id
        task = session.get(Task, uuid_obj)
        if not task:
            raise TaskNotFoundException(task_id)

        if task.owner_id != owner_id:
            raise UnauthorizedAccessException()

        # Update task fields
        for field, value in task_data.dict(exclude_unset=True).items():
            setattr(task, field, value)

        task.updated_at = task.updated_at.__class__.now()  # Update timestamp

        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Updated task {task.id} for user {owner_id}")
        return task

    @staticmethod
    def delete_task(session: Session, task_id: str, owner_id: str) -> bool:
        """
        Delete a specific task for a user
        """
        from uuid import UUID
        # Convert string ID to UUID object for proper database query
        uuid_obj = UUID(task_id) if isinstance(task_id, str) and task_id else task_id
        task = session.get(Task, uuid_obj)
        if not task:
            raise TaskNotFoundException(task_id)

        if task.owner_id != owner_id:
            raise UnauthorizedAccessException()

        session.delete(task)
        session.commit()

        logger.info(f"Deleted task {task.id} for user {owner_id}")
        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: str, completed: bool, owner_id: str) -> Task:
        """
        Toggle the completion status of a task
        """
        from uuid import UUID
        # Convert string ID to UUID object for proper database query
        uuid_obj = UUID(task_id) if isinstance(task_id, str) and task_id else task_id
        task = session.get(Task, uuid_obj)
        if not task:
            raise TaskNotFoundException(task_id)

        if task.owner_id != owner_id:
            raise UnauthorizedAccessException()

        task.completed = completed
        task.updated_at = task.updated_at.__class__.now()  # Update timestamp

        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Toggled completion status for task {task.id} for user {owner_id}")
        return task