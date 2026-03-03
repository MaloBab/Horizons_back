from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from typing import List, Optional

from .volunteer_preference import VolunteerPreferenceResponse
from .volunteer_slot import VolunteerSlotResponse

class VolunteerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    address:str
    phone_number: str

class VolunteerCreate(VolunteerBase):
    # Optionnel : si tu veux envoyer les IDs directement à la création
    # On verra dans le CRUD comment transformer ça en vraies liaisons
    pass

class VolunteerResponse(VolunteerBase):
    id: UUID
    preferences: List[VolunteerPreferenceResponse] = []
    slots: List[VolunteerSlotResponse] = []
    mates: List["VolunteerShortResponse"] = []

    model_config = ConfigDict(from_attributes=True)

class VolunteerShortResponse(BaseModel):
    """
    Version légère utilisée pour les listes d'amis ou les affectations 
    pour éviter de surcharger le JSON avec l'adresse/tel/préférences.
    """
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)