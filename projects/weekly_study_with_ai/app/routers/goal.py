from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.models import Goal
from app.schemas import GoalCreate, GoalOut


router = APIRouter(prefix = "goals", tags = ["Goals"])


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