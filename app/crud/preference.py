from sqlalchemy.orm import Session
from .. import models, schemas

def get_preference(db: Session, preference_id: int):
    return db.query(models.Preference).filter(models.Preference.id == preference_id).first()

def get_preferences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Preference).offset(skip).limit(limit).all()

def create_preference(db: Session, preference: schemas.PreferenceCreate):
    db_pref = models.Preference(label=preference.label)
    db.add(db_pref)
    db.commit()
    db.refresh(db_pref)
    return db_pref

def delete_preference(db: Session, preference_id: int):
    db_pref = get_preference(db, preference_id)
    if db_pref:
        db.delete(db_pref)
        db.commit()
        return True
    return False