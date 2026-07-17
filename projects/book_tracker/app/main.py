from fastapi import FastAPI, Depends, HTTPException
from app.models import Book
from app.schemas import BookCreate, BookRead, BookUpdate
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text, select

app = FastAPI(title = "Book Tracker")





@app.get("/health")
def status():
    return {"status" : "ok"}


@app.get("/books", response_model = list[BookRead])
def read_all_books(db:Session = Depends(get_db)):

    books = db.scalars(select(Book)).all()
    return books


@app.post("/create_book", response_model = BookRead)
def create_book(book:BookCreate,db:Session = Depends(get_db)):

    db_book = Book(**book.model_dump()) # Convert validated Pydantic data into SQLAlchemy modle.

    # Add object to current db session
    db.add(db_book)
    # Save transaction
    db.commit()
    
    # Reload object from DB to get generated values liked id
    db.refresh(db_book)

    # Return the ORM object
    return db_book

@app.put("/update_book/{book_id}", response_model=BookRead)
def update_book_by_id(
    book: BookUpdate,
    book_id: int,
    db: Session = Depends(get_db)
):
    updated_book = db.scalar(select(Book).where(Book.id == book_id))

    if updated_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book with the given id not found."
        )

    update_data = book.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(updated_book, key, value)

    db.commit()
    db.refresh(updated_book)

    return updated_book

@app.delete("/delete_book/{book_id}", response_model = BookRead)
def delete_book_by_id(
    book_id:int,
    db:Session = Depends(get_db)
):
    
    book = db.scalar(select(Book).where(Book.id == book_id))
    if book is None:
        raise HTTPException(status_code=404, detail = "Book is not found.")
    db.delete(book)
    db.commit()

    return book