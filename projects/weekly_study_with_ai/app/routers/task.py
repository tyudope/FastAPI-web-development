from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session

from sqlalchemy import select

from app.db.session import get_db
from app.models import Task, Routine
from app.schemas import TaskCreate, TaskOut


router = APIRouter(prefix = "/routines", tags = ["Tasks"])

@router.post("/{routine_id}/tasks", response_model=TaskOut)
def create_task(routine_id:int, task:TaskCreate ,db:Session = Depends(get_db)):

    #Check routine exists.
    routine = db.scalar(select(Routine).where(Routine.id == routine_id))

    if routine is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Routine with id: {routine_id} is not found in the database.")

    #Create a task with routine_id
    db_task = Task(**task.model_dump(), routine_id = routine_id)

    # Save and return.
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task
