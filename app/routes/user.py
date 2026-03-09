from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.security import get_current_admin, get_current_user
from .. import models
from uuid import UUID

from .. import crud, schemas, database

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: schemas.UserResponse = Depends(get_current_user)):
    """
    Récupère le profil complet de l'utilisateur actuellement connecté.
    Ton front-end appellera cette route à chaque chargement de l'application.
    """
    return current_user




@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Crée un nouvel utilisateur (admin ou organisateur)."""
    if crud.user.get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà enregistré."
        )
    if crud.user.get_user_by_username(db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce nom d'utilisateur est déjà pris."
        )
    return crud.user.create_user(db=db, user=user)




@router.get("/", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Récupère la liste de tous les utilisateurs (avec pagination)."""
    return crud.user.get_users(db, skip=skip, limit=limit)




@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: UUID,
              db: Session = Depends(database.get_db),
              current_user: models.User = Depends(get_current_user)):
    """Récupère un utilisateur spécifique par son ID."""
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return db_user


@router.patch("/me", response_model=schemas.UserResponse)
def update_current_user(
    user_update: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)):
    """Met à jour le profil de l'utilisateur actuellement connecté."""
    return crud.user.update_user(db=db, user_id=UUID(str(current_user.id)), user_update=user_update)




@router.patch("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: UUID,
                user_update: schemas.UserUpdate,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):
    """Met à jour les informations d'un utilisateur existant."""
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return crud.user.update_user(db=db, user_id=user_id, user_update=user_update)




@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID,
                db: Session = Depends(database.get_db),
                current_admin: models.User = Depends(get_current_admin)):
    """Supprime un utilisateur de la base de données."""
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    
    crud.user.delete_user(db=db, user_id=user_id)
    return None 