from app.database import engine
from app.models import Base

def init_db():
    Base.metadata.create_all(bind = engine)
    print("Tables created.")

if __name__ == "__main__":
    init_db()