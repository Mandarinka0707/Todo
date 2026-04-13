from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def get_todos(db: Session) -> List[models.Todo]:
    stmt = select(models.Todo).order_by(
        models.Todo.completed.asc(),
        models.Todo.priority.asc(),
        models.Todo.due_date.asc().nulls_last(),
    )
    return db.execute(stmt).scalars().all()


def get_todo(db: Session, todo_id: int) -> Optional[models.Todo]:
    return db.get(models.Todo, todo_id)


def create_todo(db: Session, todo_in: schemas.TodoCreate) -> models.Todo:
    todo = models.Todo(**todo_in.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def update_todo(
    db: Session, todo: models.Todo, todo_in: schemas.TodoUpdate
) -> models.Todo:
    for field, value in todo_in.model_dump(exclude_unset=True).items():
        setattr(todo, field, value)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo: models.Todo) -> None:
    db.delete(todo)
    db.commit()
    