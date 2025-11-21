import os
import json
from datetime import datetime

NOTES_FILE = "data/notes.json"

def add_note(title, content):
    """Save a new note."""
    os.makedirs("data", exist_ok=True)
    notes = load_notes()
    note = {"title": title, "content": content, "created": str(datetime.now())}
    notes.append(note)
    save_notes(notes)
    return f"📝 Note '{title}' saved."

def search_notes(keyword):
    """Search notes by keyword."""
    notes = load_notes()
    return [n for n in notes if keyword.lower() in n["content"].lower() or keyword.lower() in n["title"].lower()]

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)
