"""
models/job.py — ajout du champ recruitment_type absent du modèle original
"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum


class RecruitmentType(str, enum.Enum):
    Normal = "Normal"
    Specialise = "Specialise"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"))
    required_volunteers: Mapped[int] = mapped_column(default=1)
    recruitment_type: Mapped[RecruitmentType] = mapped_column(default=RecruitmentType.Normal)

    category = relationship("Category")
    slot = relationship("Slot")
    assignments = relationship("Assignment", back_populates="job")


class Assignment(Base):
    __tablename__ = "assignments"

    volunteer_id = Column(UUID(as_uuid=True), ForeignKey("volunteers.id"), primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), primary_key=True)

    volunteer = relationship("Volunteer", back_populates="assignments")
    job = relationship("Job", back_populates="assignments")