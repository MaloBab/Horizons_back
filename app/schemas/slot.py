from pydantic import BaseModel, ConfigDict, Field


class SlotBase(BaseModel):
    day_index: int = Field(..., ge=0, le=7)
    start_time: int = Field(..., ge=8, le=29)
    end_time: int = Field(..., ge=8, le=29)

    model_config = ConfigDict(from_attributes=True)


class SlotCreate(BaseModel):
    day_index: int
    start_time: int
    end_time: int


class SlotResponse(BaseModel):
    id: int
    day_index: int
    start_time: int
    end_time: int

    model_config = ConfigDict(from_attributes=True)