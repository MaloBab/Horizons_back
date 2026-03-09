from sqlalchemy.orm import Session
from uuid import UUID
from .. import models, schemas

def create_volunteer(db: Session, volunteer: schemas.VolunteerCreate):
    db_volunteer = models.volunteer.Volunteer(
        first_name=volunteer.first_name,
        last_name=volunteer.last_name,
        email=volunteer.email,
        address=volunteer.address,
        phone_number=volunteer.phone_number
    )
    
    db.add(db_volunteer)
    db.flush() 
    
    if hasattr(volunteer, "preference_ids") and volunteer.preference_ids:
        for index, pref_id in enumerate(volunteer.preference_ids):
            new_pref = models.volunteer.VolunteerPreference(
                volunteer_id=db_volunteer.id,
                preference_id=pref_id,
                rank=index + 1
            )
            db.add(new_pref)

    if hasattr(volunteer, "slot_ids") and volunteer.slot_ids:
        for s_id in volunteer.slot_ids:
            new_slot = models.volunteer.VolunteerSlot(
                volunteer_id=db_volunteer.id,
                slot_id=s_id
            )
            db.add(new_slot)

    db.commit()
    db.refresh(db_volunteer)
    return db_volunteer

def get_volunteer(db: Session, volunteer_id: UUID):
    return db.query(models.volunteer.Volunteer).filter(models.volunteer.Volunteer.id == volunteer_id).first()

def get_volunteers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.volunteer.Volunteer).offset(skip).limit(limit).all()


def delete_volunteer(db: Session, volunteer_id: UUID):
    volunteer = db.query(models.volunteer.Volunteer).filter(models.volunteer.Volunteer.id == volunteer_id).first()
    if volunteer:
        db.delete(volunteer)
        db.commit()
        return True
    return False