from pydantic import BaseModel

class PreferenceBase(BaseModel):
    label: str

class PreferenceCreate(PreferenceBase):
    pass

class PreferenceResponse(PreferenceBase):
    id: int

    class Config:
        from_attributes = True