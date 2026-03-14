from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from .. import models, schemas
from .. import crud
from ..database import get_db

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=List[schemas.JobResponse])
def list_jobs(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    return (
        db.query(models.Job)
        .options(joinedload(models.Job.category), joinedload(models.Job.slot))
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/grouped", response_model=List[schemas.CategoryGroupResponse])
def list_jobs_grouped(db: Session = Depends(get_db)):
    """
    Retourne les postes groupés par catégorie.
    Format attendu par le frontend (CategoryGroup[]).
    """
    categories = (
        db.query(models.Category)
        .order_by(models.Category.id)
        .all()
    )

    result = []
    for category in categories:
        jobs = (
            db.query(models.Job)
            .options(joinedload(models.Job.slot))
            .filter(models.Job.category_id == category.id)
            .all()
        )
        if jobs:
            result.append({"category": category, "jobs": jobs})

    return result


@router.get("/{job_id}", response_model=schemas.JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = (
        db.query(models.Job)
        .options(joinedload(models.Job.category), joinedload(models.Job.slot))
        .filter(models.Job.id == job_id)
        .first()
    )
    if not job:
        raise HTTPException(status_code=404, detail="Poste introuvable")
    return job


@router.post("/", response_model=schemas.JobResponse, status_code=201)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    # Récupère ou crée la catégorie
    category = crud.category.get_or_create_category(db, job.category)

    # Récupère ou crée le créneau
    slot = crud.slot.get_or_create_slot(db, job.slot)

    # Crée le job avec les ids résolus
    db_job = crud.job.create_job(db, job, category_id=category.id, slot_id=slot.id)
    
    return (
        db.query(models.Job)
        .options(joinedload(models.Job.category), joinedload(models.Job.slot))
        .filter(models.Job.id == db_job.id)
        .first()
    )


@router.patch("/{job_id}", response_model=schemas.JobResponse)
def update_job(job_id: int, job_update: schemas.JobUpdate, db: Session = Depends(get_db)):
    db_job = crud.job.update_job(db, job_id, job_update)
    if not db_job:
        raise HTTPException(status_code=404, detail="Poste introuvable")
    return (
        db.query(models.Job)
        .options(joinedload(models.Job.category), joinedload(models.Job.slot))
        .filter(models.Job.id == db_job.id)
        .first()
    )


@router.delete("/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    if not crud.job.delete_job(db, job_id):
        raise HTTPException(status_code=404, detail="Poste introuvable")