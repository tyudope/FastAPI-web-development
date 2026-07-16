from fastapi import FastAPI, Depends
from app.models import Book
from app.schemas import BookCreate, BookRead, BookUpdate
from app.database import SessionLocal, get_db
from app.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import text

app = FastAPI(title = "Book Tracker")





@app.get("/health")
def status():
    return {"status" : "ok"}


@app.get("/books", response_model = list[BookRead])
def read_all_books(db:Session = Depends(get_db)):

    stmt = text("SELECT * FROM book")
    result = db.execute(stmt)
    books = result.mappings().all() # rows as dict-like objects
    return books

