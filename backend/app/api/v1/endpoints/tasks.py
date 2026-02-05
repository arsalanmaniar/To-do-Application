from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import Optional
from app.services.task_service import TaskService
from app.schemas.task import (
    TaskCreate, TaskResponse, TaskUpdate, TaskCompletionUpdate, TaskListResponse, TaskFilterParams
)
from app.core.dependencies import get_current_user_id, get_db_session
from app.core.logging import logger
from datetime import datetime
import uuid

router = APIRouter()


@router.get("/tasks", response_model=TaskListResponse)
def get_tasks(
    current_user_id: str = Depends(get_current_user_id),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    session: Session = Depends(get_db_session)
):
    """
    Retrieve all tasks for the specified user
    """
    try:
        tasks, total = TaskService.get_tasks_by_user(
            session=session,
            owner_id=current_user_id,
            completed=completed,
            limit=limit,
            offset=offset
        )

        task_responses = []
        for task in tasks:
            task_response = TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                owner_id=task.owner_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            task_responses.append(task_response)

        return TaskListResponse(
            tasks=task_responses,
            total=total,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        logger.error(f"Error getting tasks for user {current_user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    """
    Create a new task for the current user
    """
    try:
        task = TaskService.create_task(
            session=session,
            task_data=task_data,
            owner_id=current_user_id
        )

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            owner_id=task.owner_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating task for user {current_user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    """
    Retrieve a specific task by ID
    """
    try:
        task = TaskService.get_task_by_id(
            session=session,
            task_id=task_id,
            owner_id=current_user_id
        )

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            owner_id=task.owner_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task {task_id} for user {current_user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    """
    Update a specific task completely
    """
    try:
        task = TaskService.update_task(
            session=session,
            task_id=task_id,
            task_data=task_data,
            owner_id=current_user_id
        )

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            owner_id=task.owner_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id} for user {current_user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def patch_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    """
    Partially update a specific task
    """
    try:
        task = TaskService.update_task(
            session=session,
            task_id=task_id,
            task_data=task_data,
            owner_id=current_user_id
        )

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            owner_id=task.owner_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error patching task {task_id} for user {current_user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    task_id: str,
    completion_data: TaskCompletionUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    """
    Toggle the completion status of a task
    """
    try:
        task = TaskService.toggle_task_completion(
            session=session,
            task_id=task_id,
            completed=completion_data.completed,
            owner_id=current_user_id
        )

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            owner_id=task.owner_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling completion for task {task_id} for user {current_user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    """
    Delete a specific task
    """
    try:
        TaskService.delete_task(
            session=session,
            task_id=task_id,
            owner_id=current_user_id
        )
        return
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id} for user {current_user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")