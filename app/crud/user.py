from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from .. import models, schemas
from ..core.security import get_password_hash

def get_user(db: Session, user_id: UUID) -> Optional[models.User]:
    """Récupère un utilisateur par son ID unique (UUID)"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Récupère un utilisateur par son nom d'utilisateur (utile pour le login)"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Récupère un utilisateur par son email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Récupère une liste d'utilisateurs avec pagination"""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Crée un nouvel utilisateur avec mot de passe haché et rôle 'user' par défaut"""
    hashed_pwd = get_password_hash(user.password)
    
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_pwd,
        role=models.UserRole.user, 
        profile_picture_url=user.profile_picture_url
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: UUID, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        if key == "password":
            setattr(db_user, "password_hash", get_password_hash(value))
        else:
            setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: UUID) -> bool:
    """Supprime un utilisateur de la base de données."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True