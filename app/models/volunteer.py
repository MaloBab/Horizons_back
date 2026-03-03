from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from .base import Base

class Volunteer(Base):
    __tablename__ = "volunteers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    preferences = relationship("VolunteerPreference", back_populates="volunteer")
    slots = relationship("VolunteerSlot", back_populates="volunteer")
    friends = relationship(
        "Volunteer", 
        secondary="volunteers_mates",
        primaryjoin="Volunteer.id==VolunteerMate.volunteer_id",
        secondaryjoin="Volunteer.id==VolunteerMate.mate_id",
        backref="is_mate_of"
    )
    
    assignments = relationship("Assignment", back_populates="volunteer")

class VolunteerPreference(Base):
    __tablename__ = "volunteer_preferences"

    volunteer_id = Column(UUID(as_uuid=True), ForeignKey("volunteers.id"), primary_key=True)
    preference_id = Column(Integer, ForeignKey("preferences.id"), primary_key=True)
    rank = Column(Integer, nullable=False)
    
    volunteer = relationship("Volunteer", back_populates="preferences")
    preference = relationship("Preference")

    __table_args__ = (
        UniqueConstraint('volunteer_id', 'rank', name='unique_volunteer_rank'),
    )
    
class VolunteerSlot(Base):
    __tablename__ = "volunteer_slots"

    volunteer_id = Column(UUID(as_uuid=True), ForeignKey("volunteers.id"), primary_key=True)
    slot_id = Column(Integer, ForeignKey("slots.id"), primary_key=True)
    volunteer = relationship("Volunteer", back_populates="slots")
    
    slot = relationship("Slot")

class VolunteerMate(Base):
    __tablename__ = "volunteers_mates"

    volunteer_id = Column(UUID(as_uuid=True), ForeignKey("volunteers.id"), primary_key=True)
    mate_id = Column(UUID(as_uuid=True), ForeignKey("volunteers.id"), primary_key=True)