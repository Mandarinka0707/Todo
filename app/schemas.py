from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = Field(ge=1, le=3, default=3, description="1-high, 2-medium, 3-low")
    due_date: Optional[date] = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = Field(default=None, ge=1, le=3)
    due_date: Optional[date] = None
    completed: Optional[bool] = None


class Todo(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

