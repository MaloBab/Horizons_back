from sqlalchemy.orm import Session
from uuid import UUID
from .. import models, schemas

def create_assignment(db: Session, assignment: schemas.AssignmentCreate):
    """Assigne un bénévole à un job"""
    db_assignment = models.job.Assignment(
        volunteer_id=assignment.volunteer_id,
        job_id=assignment.job_id
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def get_assignments_by_volunteer(db: Session, volunteer_id: UUID):
    """Récupère tous les jobs d'un bénévole (son planning)"""
    return db.query(models.job.Assignment).filter(
        models.job.Assignment.volunteer_id == volunteer_id
    ).all()

def get_assignments_by_job(db: Session, job_id: int):
    """Récupère tous les bénévoles affectés à un job précis"""
    return db.query(models.job.Assignment).filter(
        models.job.Assignment.job_id == job_id
    ).all()

def delete_assignment(db: Session, volunteer_id: UUID, job_id: int):
    """Supprime une affectation (désistement ou changement)"""
    db_assignment = db.query(models.job.Assignment).filter(
        models.job.Assignment.volunteer_id == volunteer_id,
        models.job.Assignment.job_id == job_id
    ).first()
    
    if db_assignment:
        db.delete(db_assignment)
        db.commit()
        return True
    return False