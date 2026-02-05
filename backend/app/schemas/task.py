from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: uuid.UUID
    owner_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskCompletionUpdate(BaseModel):
    completed: bool


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int
    limit: int
    offset: int


class TaskFilterParams(BaseModel):
    completed: Optional[bool] = None
    limit: Optional[int] = 50
    offset: Optional[int] = 0