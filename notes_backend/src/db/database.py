import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Determine the database URL from environment, default to local SQLite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./notes.db")


class Base(DeclarativeBase):
    """SQLAlchemy Declarative Base for ORM models."""


# For SQLite, we need check_same_thread=False when using with FastAPI/async server
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)


# PUBLIC_INTERFACE
def get_db() -> Generator:
    """Provide a database session to request handlers.

    Yields:
        Session: SQLAlchemy session bound to the configured engine.

    This is intended to be used as a FastAPI dependency, e.g.:
        def endpoint(db: Session = Depends(get_db)): ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
