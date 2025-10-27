from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Import DB components to initialize and expose get_db
from src.db.database import Base, engine, get_db  # noqa: F401
from src.db import models
from src.db.schemas import NoteCreate, NoteOut, NoteUpdate

# Load environment variables (DATABASE_URL, etc.)
load_dotenv()

app = FastAPI(
    title="Notes Backend API",
    description="Backend API for a fullstack notes app. Uses SQLAlchemy with SQLite by default.",
    version="0.1.0",
    openapi_tags=[
        {"name": "health", "description": "Health and status endpoints"},
        {"name": "notes", "description": "Notes management endpoints"},
    ],
)

# Keep CORS enabled
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Initialize database tables on application startup."""
    # Ensure all tables are created based on SQLAlchemy models
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["health"], summary="Health Check")
def health_check():
    """Simple health check endpoint returning a JSON message."""
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.get(
    "/notes",
    response_model=List[NoteOut],
    tags=["notes"],
    summary="List notes",
    description="Retrieve all notes, optionally filtering by a case-insensitive search query on title or content.",
)
def list_notes(
    q: Optional[str] = Query(default=None, description="Search query for title/content"),
    db: Session = Depends(get_db),
):
    """
    List notes with optional search.
    - q: optional search string to filter by title or content (case-insensitive).
    """
    query = db.query(models.Note)
    if q:
        # Use SQLAlchemy contains/ilike for case-insensitive search across fields
        q_like = f"%{q}%"
        query = query.filter(
            (models.Note.title.ilike(q_like)) | (models.Note.content.ilike(q_like))
        )
    query = query.order_by(models.Note.updated_at.desc())
    return query.all()


# PUBLIC_INTERFACE
@app.post(
    "/notes",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    tags=["notes"],
    summary="Create note",
    description="Create a new note with a title and optional content.",
)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note.
    Body:
      - title: required
      - content: optional (defaults to empty string)
    Returns the created note.
    """
    note = models.Note(title=payload.title, content=payload.content or "")
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
@app.get(
    "/notes/{note_id}",
    response_model=NoteOut,
    tags=["notes"],
    summary="Get note",
    description="Retrieve a single note by its ID.",
)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """
    Get a note by ID.
    Path:
      - note_id: integer ID of the note
    """
    note = db.get(models.Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@app.put(
    "/notes/{note_id}",
    response_model=NoteOut,
    tags=["notes"],
    summary="Update note",
    description="Update an existing note's title and/or content by its ID.",
)
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)):
    """
    Update a note by ID.
    Body can include any of: title, content.
    """
    note = db.get(models.Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    # Only update provided fields (partial update semantics for PUT in this simple API)
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content

    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
@app.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["notes"],
    summary="Delete note",
    description="Delete a note by its ID.",
)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """
    Delete a note by ID. Returns 204 No Content on success.
    """
    note = db.get(models.Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    db.delete(note)
    db.commit()
    # No body for 204 response
    return None
