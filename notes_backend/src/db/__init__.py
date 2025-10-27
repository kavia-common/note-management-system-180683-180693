"""
Database package initialization for notes backend.

Exposes key database components for easy import:
- Base: SQLAlchemy declarative base
- engine: SQLAlchemy engine configured from DATABASE_URL
- SessionLocal: session factory
- get_db: FastAPI dependency providing a scoped session
"""
from .database import Base, engine, SessionLocal, get_db  # noqa: F401
