from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from .. import models, schemas
from ..core.security import get_password_hash
from ..core.google_calendar import add_user_to_common_calendar

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
    hashed_pwd = get_password_hash(user.password)
    cal_id = None
    try:
        add_user_to_common_calendar(user.email)
        
    except Exception as e:
        print(f"Note : Problème d'invitation Google Agenda (Email peut-être invalide) : {e}")
        
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_pwd,
        role=models.UserRole.user, 
        profile_picture_url=user.profile_picture_url,
        calendar_id=cal_id
    )
    
    db.add(db_user)
    db.commit() 
    db.refresh(db_user)
    return db_user

#AUTHENTIFICATION GOOGLE

def get_user_by_google_sub(db: Session, google_sub: str) -> Optional[models.User]:
    """Retrouve un utilisateur par son identifiant unique Google (sub)."""
    return db.query(models.User).filter(models.User.google_sub == google_sub).first()


def link_google_account(db: Session, user: models.User, google_sub: str) -> models.User:
    """Lie un compte existant (inscription classique) à un compte Google."""
    setattr(user, "google_sub", google_sub)
    db.commit()
    db.refresh(user)
    return user


def create_oauth_user(db: Session, user_in: schemas.UserCreate, google_sub: str) -> models.User:
    """
    Crée un compte sans mot de passe, lié à Google.
    Tente aussi d'ajouter l'utilisateur au Google Calendar commun.
    """
    try:
        add_user_to_common_calendar(user_in.email)
    except Exception as e:
        print(f"Note : Problème d'invitation Google Agenda : {e}")

    db_user = models.User(
        username=user_in.username,
        email=user_in.email,
        password_hash=None,
        google_sub=google_sub,
        role=models.UserRole.user,
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