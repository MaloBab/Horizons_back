from pydantic import BaseModel, ConfigDict
from uuid import UUID
from .slot import SlotResponse

class VolunteerSlotBase(BaseModel):
    slot_id: int

class VolunteerSlotCreate(VolunteerSlotBase):
    volunteer_id: UUID

class VolunteerSlotResponse(VolunteerSlotBase):
    slot: SlotResponse
    
    model_config = ConfigDict(from_attributes=True)