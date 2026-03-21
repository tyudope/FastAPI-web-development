from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select


from app.models import Goal, Routine, Task

from app.db.session import get_db

from app.schemas.analysis import AnalysisOut
from app.services.prompt_builder import build_goal_analysis_prompt
from app.services.ai_client import analyze_text


router = APIRouter(prefix = "/analysis", tags = ["Analysis"])


@router.post("/goals/{goal_id}", response_model=AnalysisOut)
def analyze_goal(goal_id:int, db:Session = Depends(get_db)):

    goal = db.scalar(select(Goal).where(Goal.id == goal_id))

    if goal is None:
        raise HTTPException(status_code=404, detail = "Goal not found.")
    
    routine = db.scalar(select(Routine).where(Routine.goal_id == goal_id))

    if routine is None:
        raise HTTPException(status_code=404, detail = "Routine for this goal not found.")
    

    tasks = db.scalars(select(Task).where(Task.routine_id == routine.id)).all()

    prompt = build_goal_analysis_prompt(goal = goal, routine= routine, tasks = tasks)

    try:
        result = analyze_text(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Analysis failed: {str(e)}")

    return AnalysisOut(raw_response=result)

