from pydantic import BaseModel, ConfigDict
from uuid import UUID

class VolunteerMateBase(BaseModel):
    volunteer_id: UUID
    mate_id: UUID

class VolunteerMateCreate(VolunteerMateBase):
    """Utilisé pour créer un lien entre deux bénévoles"""
    pass

class VolunteerMateResponse(VolunteerMateBase):
    """Utilisé si tu as besoin de lister les paires existantes"""
    
    model_config = ConfigDict(from_attributes=True)