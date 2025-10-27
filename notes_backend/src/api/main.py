from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import DB components to initialize and expose get_db
from src.db.database import Base, engine, get_db  # noqa: F401

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
