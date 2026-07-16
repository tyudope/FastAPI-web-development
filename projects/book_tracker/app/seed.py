from app.database import SessionLocal
from app.models import Book


def seed():
    db = SessionLocal()
    try:
        books = [
            Book(name = "Dune", category = "sci-fi", total_page = 412, finished_page = 0),
            Book(name = "The Lord of the Rings: Return of the King" , 
                 category = "fantasy", total_page = 612, finished_pages = 0),
            Book(name = "Hitchiker's Guide of the Galaxy",
                 category = "sci-fi", total_page = 353, finished_page = 0),
        ]
        db.add_all(books) # stage.
        db.commit() # flush to postgresSQL
    finally:
        db.close()



if __name__ == "__main__":
    seed()

    



