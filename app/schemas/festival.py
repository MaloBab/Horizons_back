from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID

class FestivalBase(BaseModel):
    name: str
    edition: int
    start_date: date
    end_date: date
    location_name: str
    location_city: str

class FestivalCreate(FestivalBase):
    pass

class FestivalUpdate(BaseModel):
    name: Optional[str] = None
    edition: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    location_name: Optional[str] = None
    location_city: Optional[str] = None

class FestivalResponse(FestivalBase):
    id: UUID

    class Config:
        from_attributes = True