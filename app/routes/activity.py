from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from .. import crud, schemas, database
from ..core import security

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.get("/", response_model=List[schemas.ActivityResponse])
def read_activities(
    skip: int = 0, 
    limit: int = 50, 
    db: Session = Depends(database.get_db)
):
    """
    Récupère la liste des activités (triées par les plus récentes).
    Cette route est publique ou privée selon ton choix.
    """
    return crud.activity.get_activities(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_new_activity(
    activity: schemas.ActivityCreate,
    db: Session = Depends(database.get_db),
    current_user = Depends(security.get_current_user)
):
    """
    Crée une activité et l'associe automatiquement à l'utilisateur connecté.
    """
    return crud.activity.create_activity(
        db=db, 
        activity=activity, 
        user_id=current_user.id
    )

@router.delete("/old", status_code=status.HTTP_200_OK)
def delete_bulk_activities(
    limit: int = 5,
    db: Session = Depends(database.get_db),
    current_admin = Depends(security.get_current_admin)
):
    """
    Supprime les X dernières activités (Utile pour le nettoyage).
    """
    deleted_count = crud.activity.delete_old_activities(db, limit=limit)
    return {"message": f"{deleted_count} activités ont été supprimées."}

@router.get("/me", response_model=List[schemas.ActivityResponse])
def read_my_activities(
    db: Session = Depends(database.get_db),
    current_user = Depends(security.get_current_user)
):
    """
    Récupère uniquement les activités de l'utilisateur connecté.
    """
    return [a for a in crud.activity.get_activities(db) if a.user_id == current_user.id]