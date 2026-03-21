from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session

from sqlalchemy import select

from app.db.session import get_db
from app.models import Task
from app.schemas import TaskOut


router = APIRouter(prefix = "/tasks", tags = ["Tasks"])


# Get task by id 
@router.get("/{task_id}", response_model=TaskOut)
def read_task_by_id(task_id:int, db:Session = Depends(get_db)):

    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise  HTTPException(status_code = 404, detail = "Task is not found.")
    
    return task

# Get all tasks
@router.get("", response_model=list[TaskOut])
def read_tasks(db:Session = Depends(get_db)):
    
    tasks = db.scalars(select(Task)).all()

    return tasks


# Delete task by id
@router.delete("/{task_id}", response_model=TaskOut)
def delete_task_by_id(task_id:int, db:Session = Depends(get_db)):

    task = db.scalar(select(Task).where(Task.id == task_id))

    if task is None:
        raise HTTPException(status_code = 404, detail = "Task is not found.")

    db.delete(task)
    db.commit()
    
    return task


