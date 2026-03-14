"""
schemas/job.py — à remplacer intégralement
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional
from .category import CategoryCreate, CategoryResponse
from .slot import SlotResponse, SlotCreate

RecruitmentType = Literal["Normal", "Specialise"]


class JobBase(BaseModel):
    name: str = Field(..., min_length=1)
    required_volunteers: int = Field(default=1, ge=1)
    recruitment_type: RecruitmentType = "Normal"


class JobCreate(JobBase):
    category: CategoryCreate
    slot: SlotCreate


class JobUpdate(BaseModel):
    """PATCH partiel — tous les champs sont optionnels"""
    name: Optional[str] = Field(None, min_length=1)
    required_volunteers: Optional[int] = Field(None, ge=1)
    recruitment_type: Optional[RecruitmentType] = None
    category_id: Optional[int] = None
    slot_id: Optional[int] = None


class JobResponse(JobBase):
    id: int
    category_id: int
    slot_id: int
    category: CategoryResponse
    slot: SlotResponse

    model_config = ConfigDict(from_attributes=True)


class CategoryGroupResponse(BaseModel):
    """Groupe catégorie + ses postes — format attendu par le frontend"""
    category: CategoryResponse
    jobs: list[JobResponse]

    model_config = ConfigDict(from_attributes=True)