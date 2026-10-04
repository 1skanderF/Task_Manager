from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database.db import get_db
from ..schemas.tasks import TaskCreate, TasksOut, TaskUpdate, Filter
from ..models.user import Users, Tasks, Tags
from ..core.dependencies import get_current_user
from typing import Annotated

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/tasks/create")
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    """Создание задачи для конкретного пользователя"""
    max_task_id = (
        db.query(func.max(Tasks.user_task_number))
        .filter(Tasks.user_id == current_user.id)
        .scalar()
    ) or 0

    task = Tasks(
        user_id=current_user.id,
        user_task_number=max_task_id + 1,
        title=task_data.title,
        description=task_data.description,
    )

    if task_data.tag:
        tag = db.query(Tags).filter(Tags.name == task_data.tag).first()
        if tag is None:
            tag = Tags(name=task_data.tag)
            db.add(tag)
            db.flush()
        task.tag = tag

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/tasks", response_model=list[TasksOut])
def tasks(
    filter: Annotated[Filter, Query()],
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    q = db.query(Tasks).filter(Tasks.user_id == current_user.id)

    if filter.tag is not None:
        q = q.join(Tags).filter(Tags.name == filter.tag)

    if filter.limit is not None:
        q = q.limit(filter.limit)

    return q.all()

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    task = (
        db.query(Tasks)
        .filter(
            Tasks.user_id == current_user.id,
            Tasks.user_task_number == task_id,
        )
        .first()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}


@router.patch("/tasks/{task_id}")
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    task = (
        db.query(Tasks)
        .filter(
            Tasks.user_id == current_user.id,
            Tasks.user_task_number == task_id,
        )
        .first()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.tag is not None:
        tag = db.query(Tags).filter(Tags.name == task_data.tag).first()
        if tag is None:
            tag = Tags(name=task_data.tag)
            db.add(tag)
            db.flush()
        task.tag = tag

    db.commit()
    db.refresh(task)
    return task