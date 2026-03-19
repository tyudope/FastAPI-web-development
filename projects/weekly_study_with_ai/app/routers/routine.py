from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models import Goal, Routine
from app.schemas import RoutineCreate, RoutineOut


router = APIRouter(prefix = "/goals", tags = ["Routines"]) # This means all routes inside will start with: /goals

@router.post("/{goal_id}/routine", response_model=RoutineOut)
def create_routine_for_goal(goal_id:int, routine:RoutineCreate, db:Session = Depends(get_db)):

    # Check if the goal exists
    goal = db.scalar(select(Goal).where(Goal.id == goal_id))
    if goal is None:
        raise HTTPException(status_code= 404, detail = "Goal not found.")

    # Check if this goal already has a routine (one-to-one rule)
    existing_routine = db.scalar(select(Routine).where(Routine.goal_id == goal_id))
    if existing_routine is not None:
        raise HTTPException(status_code=400, detail = "The goal already has a routine.")
    

    # Create a routine linked to the goal
    db_routine = Routine(**routine.model_dump(), goal_id = goal_id)

    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)

    return db_routine