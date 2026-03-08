from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from .. import schemas, models, crud, database
from ..core import security

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# ── Helpers ───────────────────────────────────────────────────────────────────

def _task_query(db: Session):
    """Base query with all relations needed for TaskResponse pre-loaded."""
    return (
        db.query(models.Task)
        .options(
            joinedload(models.Task.tags),
            joinedload(models.Task.subtasks),
            joinedload(models.Task.assignee),
        )
    )

def _get_task_or_404(db: Session, task_id: UUID) -> models.Task:
    task = _task_query(db).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    return task


# ── CRUD ──────────────────────────────────────────────────────────────────────

@router.post("/", response_model=schemas.task.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: schemas.task.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    task = crud.task.create_task(db=db, task_in=task_in, creator_id=current_user.id)
    return _get_task_or_404(db, task.id)


@router.get("/", response_model=List[schemas.task.TaskResponse])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    status: models.TaskStatus | None = None,
    assignee_id: UUID | None = None,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    query = _task_query(db)
    if status:
        query = query.filter(models.Task.status == status)
    if assignee_id:
        query = query.filter(models.Task.assignee_id == assignee_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{task_id}", response_model=schemas.task.TaskResponse)
def read_task(
    task_id: UUID,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    return _get_task_or_404(db, task_id)


@router.put("/{task_id}", response_model=schemas.task.TaskResponse)
def update_task_full(
    task_id: UUID,
    task_in: schemas.task.TaskUpdate,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    db_task = _get_task_or_404(db, task_id)
    try:
        crud.task.update_task(db=db, db_task=db_task, task_in=task_in, current_user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _get_task_or_404(db, task_id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_route(
    task_id: UUID,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    if not crud.task.delete_task(db=db, task_id=task_id):
        raise HTTPException(status_code=404, detail="Tâche introuvable")


# ── Specific actions ──────────────────────────────────────────────────────────

@router.patch("/{task_id}/status", response_model=schemas.task.TaskResponse)
def change_task_status(
    task_id: UUID,
    new_status: models.TaskStatus,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    db_task = _get_task_or_404(db, task_id)
    task_in = schemas.task.TaskUpdate(status=new_status)
    crud.task.update_task(db=db, db_task=db_task, task_in=task_in, current_user_id=current_user.id)
    return _get_task_or_404(db, task_id)


@router.patch("/{task_id}/assign", response_model=schemas.task.TaskResponse)
def assign_task(
    task_id: UUID,
    assignee_id: UUID | None = None,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    db_task = _get_task_or_404(db, task_id)
    task_in = schemas.task.TaskUpdate(assignee_id=assignee_id)
    crud.task.update_task(db=db, db_task=db_task, task_in=task_in, current_user_id=current_user.id)
    return _get_task_or_404(db, task_id)


# ── Audit logs ────────────────────────────────────────────────────────────────

@router.get("/{task_id}/audit-logs", response_model=List[schemas.task.TaskAuditLogResponse])
def get_task_history(
    task_id: UUID,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    _get_task_or_404(db, task_id)  # 404 guard
    return (
        db.query(models.TaskAuditLog)
        .options(joinedload(models.TaskAuditLog.actor))
        .filter(models.TaskAuditLog.task_id == task_id)
        .order_by(models.TaskAuditLog.created_at.asc())
        .all()
    )


# ── Comments ──────────────────────────────────────────────────────────────────

@router.post("/{task_id}/comments", response_model=schemas.task.TaskCommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment(
    task_id: UUID,
    comment_in: schemas.task.TaskCommentCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    _get_task_or_404(db, task_id)  # 404 guard

    new_comment = models.TaskComment(
        task_id=task_id,
        author_id=current_user.id,
        content=comment_in.content,
    )
    db.add(new_comment)
    db.commit()

    # db.refresh() does NOT load relationships — re-query with joinedload instead
    new_comment = (
        db.query(models.TaskComment)
        .options(joinedload(models.TaskComment.author))
        .filter(models.TaskComment.id == new_comment.id)
        .one()
    )
    return new_comment


@router.get("/{task_id}/comments", response_model=List[schemas.task.TaskCommentResponse])
def get_task_comments(
    task_id: UUID,
    db: Session = Depends(database.get_db),
    current_user=Depends(security.get_current_user),
):
    _get_task_or_404(db, task_id)  # 404 guard
    return (
        db.query(models.TaskComment)
        .options(joinedload(models.TaskComment.author))
        .filter(models.TaskComment.task_id == task_id)
        .order_by(models.TaskComment.created_at.asc())
        .all()
    )