from sqlalchemy.orm import Session
from .. import models, schemas

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def get_or_create_category(db: Session, category_data: schemas.CategoryCreate):
    existing = db.query(models.Category).filter(
        models.Category.label == category_data.label,
    ).first()
    
    if existing:
        return existing
    
    db_category = models.Category(**category_data.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def create_category(db: Session, category: schemas.CategoryBase):
    db_category = models.Category(label=category.label)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False