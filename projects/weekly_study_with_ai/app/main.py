from fastapi import FastAPI
from app.db.session import engine
from app.models import Base




from app.routers.goal import router as goal_router # Add Goal Router




app = FastAPI(title = "Study with AI")


@app.get("/health")
def health():
    return {"Status " : "ok"}



@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind = engine)


app.include_router(goal_router)