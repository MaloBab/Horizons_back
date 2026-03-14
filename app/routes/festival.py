from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from ..core.security import get_current_user, get_current_admin
from .. import models

router = APIRouter(prefix="/festival", tags=["Festival"])


@router.get("/", response_model=schemas.FestivalResponse)
def read_festival(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Récupère les infos du festival. Accessible à tous les utilisateurs connectés."""
    festival = crud.festival.get_festival(db)
    if not festival:
        raise HTTPException(status_code=404, detail="Aucun festival configuré.")
    return festival


@router.post("/", response_model=schemas.FestivalResponse, status_code=status.HTTP_201_CREATED)
def create_festival(
    festival: schemas.FestivalCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Crée le festival."""
    if crud.festival.get_festival(db):
        raise HTTPException(status_code=400, detail="Un festival existe déjà. Utilisez PATCH pour le modifier.")
    return crud.festival.create_festival(db, festival)


@router.patch("/", response_model=schemas.FestivalResponse)
def update_festival(
    festival_update: schemas.FestivalUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Met à jour le festival."""
    festival = crud.festival.update_festival(db, festival_update)
    if not festival:
        raise HTTPException(status_code=404, detail="Aucun festival configuré.")
    return festival


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_festival(
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(get_current_admin),
):
    """Supprime le festival. Admin uniquement."""
    if not crud.festival.delete_festival(db):
        raise HTTPException(status_code=404, detail="Aucun festival configuré.")
    return None