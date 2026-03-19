from fastapi import APIRouter, Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models import Goal
from app.schemas import GoalCreate, GoalOut

from typing import List



router = APIRouter(prefix = "/goals", tags = ["Goals"])


# Create a new goal
@router.post("", response_model = GoalOut)
def create_goal(goal: GoalCreate, db:Session = Depends(get_db)):

    db_goal = Goal(**goal.model_dump()) # convert goal (pydantic object) to SQLAlchemy ORM object

    # Add objec to curent db session
    db.add(db_goal)

    # Save transaction permanently
    db.commit()

    # Reload object from DB to get generated values like id
    db.refresh(db_goal)

    # Return ORM(Goal) object : FastAPI converts it to the GoalOut(pydantic object)
    return db_goal




# Gets all the goals
@router.get("", response_model = list[GoalOut])
def read_goals(db:Session = Depends(get_db)):
    goals = db.scalars(select(Goal)).all()
    return goals


# Get a goal with the given id
@router.get("/{goal_id}", response_model = GoalOut)
def read_goal_by_id(goal_id:int ,db:Session = Depends(get_db)):
    
    goal = db.scalar(select(Goal).where(Goal.id == goal_id))

    if goal is None:
        raise HTTPException(status_code=404, detail = f"Goal with id : {goal_id} is not found in our database. ")
    
    return goal



