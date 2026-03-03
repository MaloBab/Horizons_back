from pydantic import BaseModel, ConfigDict, Field
from .category import CategoryResponse
from .slot import SlotResponse

class JobBase(BaseModel):
    name: str = Field(..., min_length=1) # On s'assure que le nom n'est pas vide
    required_volunteers: int = Field(default=1, ge=1)

class JobCreate(JobBase):
    category_id: int
    slot_id: int

class JobResponse(JobBase):
    id: int
    category_id: int
    slot_id: int
    category: CategoryResponse 
    slot: SlotResponse

    model_config = ConfigDict(from_attributes=True)