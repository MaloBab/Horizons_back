from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.schemas.user import UserShortResponse


class ActivityBase(BaseModel):
    icon : Optional[str] = None
    title : str
    action_type : str
    user_id : UUID

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: int
    created_at: datetime
    user_id: UUID
    # Ici, Pydantic va chercher l'objet "user" dans ton modèle SQLAlchemy
    user: UserShortResponse 

    class Config:
        from_attributes = True