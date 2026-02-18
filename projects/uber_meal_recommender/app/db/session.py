from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


# SQLite needs this for FastAPI (multi-threaded server)
connect_args = {"check_same_thread":False} if settings.database_url.startswith("sqlite") else {}


engine = create_engine(
    url= settings.database_url,
    connect_args=connect_args,
    echo = False, # set True if you want SQL logs.
)

SessionLocal = sessionmaker(bind = engine, autoflush=False, autocommit= False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:    
        db.close