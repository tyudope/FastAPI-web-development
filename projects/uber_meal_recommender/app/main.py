from fastapi import FastAPI
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models.order import Order
from app.seed import seed_orders

app = FastAPI(title = "Uber Meal Recommender")


@app.get("/health")
def health():
    return {"status": "ok"}



# Temprorary create all
@app.on_event("startup")
def on_startup():
    # Create a tables.
    Base.metadata.create_all(bind = engine)

    # seed database.
    db = SessionLocal()
    try:
        seed_orders(db)
    finally:
        db.close()
    
