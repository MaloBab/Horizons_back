from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base
from sqlalchemy.dialects.postgresql import UUID

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)
    required_volunteers = Column(Integer, nullable=False)

    category = relationship("Category")
    slot = relationship("Slot")
    assignments = relationship("Assignment", back_populates="job")
    
class Assignment(Base):
    __tablename__ = "assignments"

    volunteer_id = Column(UUID(as_uuid=True), ForeignKey("volunteers.id"), primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), primary_key=True)
    
    volunteer = relationship("Volunteer", back_populates="assignments")
    job = relationship("Job", back_populates="assignments")