from sqlalchemy.orm import Session
from .. import models, schemas

def get_festival(db: Session) -> models.Festival | None:
    """Récupère le festival (table à ligne unique)."""
    return db.query(models.Festival).first()

def create_festival(db: Session, festival: schemas.FestivalCreate) -> models.Festival:
    db_festival = models.Festival(**festival.model_dump())
    db.add(db_festival)
    db.commit()
    db.refresh(db_festival)
    return db_festival

def update_festival(db: Session, festival_update: schemas.FestivalUpdate) -> models.Festival | None:
    db_festival = db.query(models.Festival).first()
    if not db_festival:
        return None
    for key, value in festival_update.model_dump(exclude_unset=True).items():
        setattr(db_festival, key, value)
    db.commit()
    db.refresh(db_festival)
    return db_festival

def delete_festival(db: Session) -> bool:
    db_festival = db.query(models.Festival).first()
    if not db_festival:
        return False
    db.delete(db_festival)
    db.commit()
    return True