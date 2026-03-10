from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from ..models import TaskStatus, TaskPriority, TaskType


# ── Tags ──────────────────────────────────────────────────────────────────────

class TagBase(BaseModel):
    name: str
    color_hex: Optional[str] = None

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ── User (embedded in responses) ──────────────────────────────────────────────
# Minimal shape used inside TaskCommentResponse
# so the frontend doesn't need a second round-trip to resolve author/actor.

class UserEmbedded(BaseModel):
    id: UUID
    username: str
    profile_picture_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# ── Comments ──────────────────────────────────────────────────────────────────

class TaskCommentCreate(BaseModel):
    content: str = Field(..., min_length=1)

class TaskCommentResponse(BaseModel):
    id: int
    task_id: UUID
    author_id: UUID
    author: UserEmbedded          # ✅ embedded so frontend gets username directly
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class SubtaskResponse(BaseModel):
    id: int
    title: str
    is_completed: bool
    position: int
    model_config = ConfigDict(from_attributes=True)


# ── Tasks ─────────────────────────────────────────────────────────────────────

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    type: TaskType = TaskType.STANDARD
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

class SubtaskUpsert(BaseModel):
    id: Optional[int] = None
    title: str
    is_completed: bool = False
    position: int = 0

class TaskCreate(TaskBase):
    assignee_id: Optional[UUID] = None
    tag_ids: Optional[List[int]] = []
    subtasks: Optional[List[SubtaskUpsert]] = []


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[TaskType] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[UUID] = None
    due_date: Optional[datetime] = None
    tag_ids: Optional[List[int]] = None
    subtasks: Optional[List[SubtaskUpsert]] = None

class TaskResponse(TaskBase):
    id: UUID
    status: TaskStatus
    creator_id: UUID
    assignee_id: Optional[UUID] = None
    assignee: Optional[UserEmbedded] = None
    opened_at: datetime
    verification_opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    tags: List[TagResponse] = []
    subtasks: List[SubtaskResponse] = []
    model_config = ConfigDict(from_attributes=True)