from pydantic import BaseModel

class SlotBase(BaseModel):
    start_time: int
    end_time: int
    day_of_week: int
    
class SlotCreate(SlotBase):
    pass

class SlotResponse(SlotBase):
    id: int

    class Config:
        from_attributes = True
    