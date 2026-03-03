from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from .preference import PreferenceResponse

class VolunteerPreferenceBase(BaseModel):
    preference_id: int
    rank: int = Field(..., ge=1, description="Le rang de préférence (1 étant le plus haut)")

class VolunteerPreferenceCreate(VolunteerPreferenceBase):
    volunteer_id: UUID

class VolunteerPreferenceResponse(VolunteerPreferenceBase):
    preference: PreferenceResponse
    
    model_config = ConfigDict(from_attributes=True)