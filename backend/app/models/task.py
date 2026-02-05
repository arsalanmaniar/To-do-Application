from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task model representing a user's todo item
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user (owner)
    owner: Optional["User"] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """
    Schema for creating a new task
    """
    pass


class TaskRead(TaskBase):
    """
    Schema for reading a task
    """
    id: uuid.UUID
    owner_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """
    Schema for updating a task (all fields optional for partial updates)
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: Optional[bool] = Field(default=None)