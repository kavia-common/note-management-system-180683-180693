from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Shared properties for Note create/update."""
    title: Optional[str] = Field(default=None, description="Title of the note")
    content: Optional[str] = Field(default=None, description="Content of the note")


class NoteCreate(NoteBase):
    """Schema for creating a new Note."""
    title: str = Field(..., description="Title of the note")
    content: Optional[str] = Field(default="", description="Content of the note")


class NoteUpdate(NoteBase):
    """Schema for updating an existing Note."""
    pass


class NoteOut(BaseModel):
    """Schema for returning a Note via API."""
    id: int = Field(..., description="Unique identifier")
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content of the note")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
