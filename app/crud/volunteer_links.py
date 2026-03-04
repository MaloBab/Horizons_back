from sqlalchemy.orm import Session
from uuid import UUID
from .. import models

# --- PREFERENCES ---
def add_preference_to_volunteer(db: Session, volunteer_id: UUID, preference_id: int, rank: int):
    db_link = models.volunteer.VolunteerPreference(volunteer_id=volunteer_id, preference_id=preference_id, rank=rank)
    db.add(db_link)
    db.commit()
    return db_link

def remove_preference_from_volunteer(db: Session, volunteer_id: UUID, preference_id: int):
    db_link = db.query(models.volunteer.VolunteerPreference).filter_by(volunteer_id=volunteer_id, preference_id=preference_id).first()
    if db_link:
        db.delete(db_link)
        db.commit()

# --- SLOTS ---
def add_slot_to_volunteer(db: Session, volunteer_id: UUID, slot_id: int):
    db_link = models.volunteer.VolunteerSlot(volunteer_id=volunteer_id, slot_id=slot_id)
    db.add(db_link)
    db.commit()
    return db_link

def remove_slot_from_volunteer(db: Session, volunteer_id: UUID, slot_id: int):
    db_link = db.query(models.volunteer.VolunteerSlot).filter_by(volunteer_id=volunteer_id, slot_id=slot_id).first()
    if db_link:
        db.delete(db_link)
        db.commit()

# --- MATES (BINÔMES) ---
def add_mate_to_volunteer(db: Session, volunteer_id: UUID, mate_id: UUID):
    db_link = models.volunteer.VolunteerMate(volunteer_id=volunteer_id, mate_id=mate_id)
    db.add(db_link)
    db.commit()
    return db_link

def remove_mate_from_volunteer(db: Session, volunteer_id: UUID, mate_id: UUID):
    db_link = db.query(models.volunteer.VolunteerMate).filter_by(volunteer_id=volunteer_id, mate_id=mate_id).first()
    if db_link:
        db.delete(db_link)
        db.commit()