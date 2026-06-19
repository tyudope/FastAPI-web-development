from fastapi import FastAPI, HTTPException

from app.schemas import PlanRequest, PlanResponse
from app.service import generate_date_plan, PlanGenerationError


app = FastAPI(title = "Date Night Generator")

@app.post("/date-night")
def date_night(req: PlanRequest) -> PlanResponse:
    try:
        return generate_date_plan(req)
    except PlanGenerationError as e:
        raise HTTPException(
            status_code=502,
            detail = "The planner returned an invalid response. Please try again.",
            ) from e




