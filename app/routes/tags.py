from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, database
from ..core import security

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("/", response_model=List[schemas.task.TagResponse])
def read_tags(
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    """
    Récupère la liste de tous les tags disponibles (triés par nom).
    """
    return db.query(models.Tag).order_by(models.Tag.name).all()


@router.post("/", response_model=schemas.task.TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_in: schemas.task.TagCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    """
    Crée un nouveau tag. Le nom doit être unique.
    """
    existing = db.query(models.Tag).filter(models.Tag.name == tag_in.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un tag avec ce nom existe déjà."
        )
    tag = models.Tag(**tag_in.model_dump())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.patch("/{tag_id}", response_model=schemas.task.TagResponse)
def update_tag(
    tag_id: int,
    tag_in: schemas.task.TagCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    """
    Modifie le nom ou la couleur d'un tag existant.
    Réservé aux admins.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès réservé aux admins.")

    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag introuvable.")

    for key, value in tag_in.model_dump(exclude_unset=True).items():
        setattr(tag, key, value)
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    """
    Supprime un tag (admin uniquement).
    Le tag est automatiquement retiré de toutes les tâches via CASCADE.
    """
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag introuvable.")
    db.delete(tag)
    db.commit()