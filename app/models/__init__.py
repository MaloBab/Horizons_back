from .base import Base

from .user import User, UserRole
from .volunteer import Volunteer
from .activity import Activity
from .preference import Preference
from .category import Category
from .slot import Slot
from .job import Job
from .task import Task, TaskComment, Subtask, TaskAttachment, TaskAuditLog, TaskPriority, TaskStatus, TaskType, Tag

# Cette liste optionnelle permet de définir ce qui est exporté 
# quand on fait "from app.models import *"
__all__ = [
    "Base",
    "User",
    "UserRole",
    "Volunteer",
    "Activity",
    "Preference",
    "Category",
    "Slot",
    "Job",
    "Task",
    "TaskComment",
    "Subtask",
    "TaskAttachment",
    "TaskAuditLog",
    "Tag",
    "TaskPriority",
    "TaskStatus",
    "TaskType",
]