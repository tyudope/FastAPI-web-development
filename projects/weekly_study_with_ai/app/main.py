from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.db.session import engine
from app.models import Base

from app.routers.goal import router as goal_router
from app.routers.routine import router as routine_router
from app.routers.task import router as task_router
from app.routers.analysis import router as analysis_router


app = FastAPI(title = "Study with AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def index():
    with open("static/index.html") as f:
        return f.read()


@app.get("/health")
def health():
    return {"Status" : "ok"}



@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind = engine)


app.include_router(goal_router)
app.include_router(routine_router)
app.include_router(task_router)
app.include_router(analysis_router)