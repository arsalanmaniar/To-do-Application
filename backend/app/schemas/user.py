from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    id: str
    email: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    created_at: datetime