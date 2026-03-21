from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models import Routine, Task
from app.schemas import RoutineOut, TaskCreate, TaskOut


router = APIRouter(prefix = "/routines", tags = ["Routines"]) # This means all routes inside will start with: /routines

# Get all routines
@router.get("" , response_model = list[RoutineOut])
def read_routines(db:Session = Depends(get_db)):
    
    routines = db.scalars(select(Routine)).all()

    return routines


# Get routine by id
@router.get("/{routine_id}", response_model=RoutineOut)
def read_routine_by_id(routine_id:int, db:Session = Depends(get_db)):

    routine = db.scalar(select(Routine).where(Routine.id == routine_id))

    if routine is None:
        raise HTTPException(status_code = 404, detail = f"Routine with id : {routine_id} is not found in the database.")


    return routine

# Delete routine by id
@router.delete("/{routine_id}", response_model=RoutineOut)
def delete_routine_by_id(routine_id:int, db:Session = Depends(get_db)):

    routine = db.scalar(select(Routine).where(Routine.id == routine_id ))

    if routine is None:
        raise HTTPException(status_code=404, detail = "Routine was not found.")


    db.delete(routine)
    db.commit()
    return routine

# Create a task for a routine
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