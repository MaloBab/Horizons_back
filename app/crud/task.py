from sqlalchemy.orm import Session
from datetime import datetime, timezone
from .. import schemas, models
from uuid import UUID


# ==========================================
# 1. CRÉER (CREATE)
# ==========================================

def create_task(db: Session, task_in: schemas.task.TaskCreate, creator_id: str) -> models.Task:
    # exclude_none évite de passer assignee_id=None, due_date=None etc. au constructeur
    task_data = task_in.model_dump(exclude={"tag_ids"}, exclude_none=True)

    db_task = models.Task(**task_data, creator_id=creator_id)

    if task_in.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(task_in.tag_ids)).all()
        db_task.tags = tags

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    log = models.TaskAuditLog(
        task_id=db_task.id,
        user_id=creator_id,
        action="task_created",
        new_value=db_task.status.value,
    )
    db.add(log)
    db.commit()

    return db_task


# ==========================================
# 2. LIRE (READ)
# ==========================================

def get_task(db: Session, task_id: UUID) -> models.Task | None:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: models.TaskStatus | None = None,
    assignee_id: str | None = None,
) -> list[models.Task]:
    query = db.query(models.Task)
    if status:
        query = query.filter(models.Task.status == status)
    if assignee_id:
        query = query.filter(models.Task.assignee_id == assignee_id)
    return query.offset(skip).limit(limit).all()


# ==========================================
# 3. METTRE À JOUR (UPDATE)
# ==========================================

def update_task(
    db: Session,
    db_task: models.Task,
    task_in: schemas.task.TaskUpdate,
    current_user_id: UUID,
) -> models.Task:
    update_data = task_in.model_dump(exclude_unset=True, exclude={"tag_ids", "subtasks"})

    # Règle : l'assigné ne peut pas être le vérificateur
    new_assignee = update_data.get("assignee_id", db_task.assignee_id)
    # Dates automatiques au changement de statut
    if "status" in update_data and update_data["status"] != db_task.status:
        new_status = update_data["status"]
        if new_status == models.TaskStatus.REVIEW:       # ✅ était TO_VERIFY
            update_data["verification_opened_at"] = datetime.now(timezone.utc)
        elif new_status == models.TaskStatus.CLOSED:
            update_data["closed_at"] = datetime.now(timezone.utc)
        elif new_status == models.TaskStatus.OPEN:
            update_data["closed_at"] = None

    # Mise à jour des champs + logs
    for key, value in update_data.items():
        old_value = getattr(db_task, key)
        if old_value != value:
            setattr(db_task, key, value)
            db.add(models.TaskAuditLog(
                task_id=db_task.id,
                user_id=current_user_id,
                action=f"{key}_updated",
                old_value=str(old_value) if old_value is not None else None,
                new_value=str(value) if value is not None else None,
            ))

    # ✅ Correction : models.Tag  (pas models.Task.Tag)
    if task_in.tag_ids is not None:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(task_in.tag_ids)).all()
        db_task.tags = tags
        db.add(models.TaskAuditLog(
            task_id=db_task.id,
            user_id=current_user_id,
            action="tags_updated",
        ))

    # ── Sous-tâches ────────────────────────────────────────────────────────────
    if task_in.subtasks is not None:
        # Supprime toutes les sous-tâches existantes puis recrée
        # (stratégie simple : évite de gérer les diff id-par-id)
        for existing in list(db_task.subtasks):
            db.delete(existing)
        db.flush()   # libère les ids avant d'insérer les nouveaux

        for sub in task_in.subtasks:
            db.add(models.Subtask(
                task_id=db_task.id,
                title=sub.title,
                is_completed=sub.is_completed,
                position=sub.position,
            ))

    db.commit()
    db.refresh(db_task)
    return db_task


# ==========================================
# 4. SUPPRIMER (DELETE)
# ==========================================

def delete_task(db: Session, task_id: UUID) -> bool:
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False