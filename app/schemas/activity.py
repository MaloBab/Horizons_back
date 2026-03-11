from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.schemas.user import UserShortResponse


class ActivityBase(BaseModel):
    title : str
    action_type : str

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: int
    created_at: datetime
    user_id: UUID
    author: UserShortResponse 

    class Config:
        from_attributes = True