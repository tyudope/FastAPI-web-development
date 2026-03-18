from sqlalchemy import create_engine # creates a database connection manager
from sqlalchemy.orm import sessionmaker # sessionmaker creates a database sessions.
from app.core.config import settings # This import configuration we explained earlier.



# Must have for SQLite
connect_args = {"check_same_thread" : False} if settings.database_url.startswith("sqlite") else {}



# Create the engine
# This creates a SQLAlchemy engine, (connect databases, manage connection pool, execute sql statements.)
engine = create_engine(
    url = settings.database_url,
    connect_args=connect_args,
    echo=False
)


# This creates a session factory
# SessionLocal() -> creates a new session.
SessionLocal = sessionmaker(
    bind = engine,
    autoflush=False,
    autocommit=False
)


# Dependency injection

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


