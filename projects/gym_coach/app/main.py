from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.schemas import WorkoutRequest, WorkoutResponse
from app.service import generate_workout_plan, PlanGenerationError


STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

app = FastAPI(title = "Workout Plan Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return (STATIC_DIR / "index.html").read_text(encoding="utf-8")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/workout-plan")
def workout_plan(req: WorkoutRequest) -> WorkoutResponse:
    try:
        return generate_workout_plan(req)
    except PlanGenerationError as e:
        raise HTTPException(
            status_code=502,
            detail = "The planner returned an invalid response. Please try again.",
        ) from e

