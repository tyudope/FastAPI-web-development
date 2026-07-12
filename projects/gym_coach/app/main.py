from fastapi import FastAPI, HTTPException

from app.schemas import WorkoutRequest, WorkoutResponse
from app.service import generate_workout_plan, PlanGenerationError



app = FastAPI(title = "Workout Plan Generator")



@app.post("/workout-plan")
def workout_plan(req: WorkoutRequest) -> WorkoutResponse:
    try:
        generate_workout_plan(req)
    except PlanGenerationError as e:
        raise HTTPException(
            status_code=502,
            detail = "The planner returned an invalid response. Please try again.",
        ) from e
    

