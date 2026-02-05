from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class UserBase(SQLModel):
    id: str = Field(primary_key=True)
    email: str = Field(nullable=False)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """
    User model representing a registered user
    """
    created_at: datetime = Field(default_factory=datetime.utcnow)
    hashed_password: str = Field()

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="owner")


class UserRead(UserBase):
    """
    Schema for reading user information
    """
    created_at: datetime