from sqlalchemy.orm import Session
from uuid import UUID
from .. import models, schemas

def get_activities(db: Session, skip: int = 0, limit: int = 50):
    # On trie par ordre décroissant pour avoir les plus récents en premier
    return db.query(models.Activity).order_by(models.Activity.created_at.desc()).offset(skip).limit(limit).all()

def create_activity(db: Session, activity: schemas.ActivityCreate, user_id: UUID):
    db_activity = models.Activity(
        **activity.model_dump(), 
        user_id=user_id
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def delete_old_activities(db: Session, limit: int):
    """Supprime les 'x' (limit) activités les plus anciennes du feed."""
    
    old_activities = db.query(models.Activity.id)\
                       .order_by(models.Activity.created_at.asc())\
                       .limit(limit)\
                          .all()
    
    if not old_activities:
        return 0

    old_ids = [activity.id for activity in old_activities]
    
    deleted_count = db.query(models.Activity)\
                      .filter(models.Activity.id.in_(old_ids))\
                      .delete(synchronize_session=False)         
    db.commit()
    
    return deleted_count