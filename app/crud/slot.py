from sqlalchemy.orm import Session
from .. import models, schemas

def get_slot(db: Session, slot_id: int):
    return db.query(models.Slot).filter(models.Slot.id == slot_id).first()

def get_slots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Slot).offset(skip).limit(limit).all()

def create_slot(db: Session, slot: schemas.SlotCreate):
    db_slot = models.Slot(**slot.model_dump())
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

def update_slot(db: Session, slot_id: int, slot_update: schemas.SlotBase):
    db_slot = get_slot(db, slot_id)
    if db_slot:
        for key, value in slot_update.model_dump(exclude_unset=True).items():
            setattr(db_slot, key, value)
        db.commit()
        db.refresh(db_slot)
    return db_slot