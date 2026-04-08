from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.src import crud, schemas
from app.src.db import get_db

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("", response_model=list[schemas.Todo])
def list_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)


@router.get("/{todo_id}", response_model=schemas.Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.post("", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo_in: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo_in)


@router.put("/{todo_id}", response_model=schemas.Todo)
def update_todo(
    todo_id: int, todo_in: schemas.TodoUpdate, db: Session = Depends(get_db)
):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return crud.update_todo(db, todo, todo_in)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    crud.delete_todo(db, todo)

