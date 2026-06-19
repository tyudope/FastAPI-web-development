from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.schemas import PlanRequest, PlanResponse
from app.service import generate_date_plan, PlanGenerationError


STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

app = FastAPI(title = "Date Night Generator")

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


@app.post("/date-night")
def date_night(req: PlanRequest) -> PlanResponse:
    try:
        return generate_date_plan(req)
    except PlanGenerationError as e:
        raise HTTPException(
            status_code=502,
            detail = "The planner returned an invalid response. Please try again.",
            ) from e
