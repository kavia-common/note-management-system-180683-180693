/**
 * API client utilities for the Notes frontend.
 * Reads the API base URL from REACT_APP_API_BASE_URL, defaults to http://localhost:3001.
 */

// PUBLIC_INTERFACE
export function getApiBaseUrl() {
  /** Returns the backend API base URL from env or default. */
  const envUrl = process.env.REACT_APP_API_BASE_URL;
  return (envUrl && envUrl.trim()) || "http://localhost:3001";
}

const API_BASE = getApiBaseUrl();

// PUBLIC_INTERFACE
export async function fetchNotes(q) {
  /** Fetch list of notes, optionally filtered by a search query. */
  const url = new URL("/notes", API_BASE);
  if (q && q.trim()) url.searchParams.set("q", q.trim());

  const res = await fetch(url.toString(), {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error(`Failed to fetch notes: ${res.status}`);
  return res.json();
}

// PUBLIC_INTERFACE
export async function createNote({ title, content = "" }) {
  /** Create a new note with title and optional content. */
  const res = await fetch(new URL("/notes", API_BASE).toString(), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content }),
  });
  if (!res.ok) throw new Error(`Failed to create note: ${res.status}`);
  return res.json();
}

// PUBLIC_INTERFACE
export async function updateNote(id, { title, content }) {
  /** Update an existing note by id; supports partial fields. */
  const res = await fetch(new URL(`/notes/${id}`, API_BASE).toString(), {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content }),
  });
  if (!res.ok) throw new Error(`Failed to update note ${id}: ${res.status}`);
  return res.json();
}

// PUBLIC_INTERFACE
export async function deleteNote(id) {
  /** Delete a note by id. Returns void on success. */
  const res = await fetch(new URL(`/notes/${id}`, API_BASE).toString(), {
    method: "DELETE",
  });
  if (!res.ok) throw new Error(`Failed to delete note ${id}: ${res.status}`);
}
