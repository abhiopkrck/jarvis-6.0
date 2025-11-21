import datetime
import json
import os

CALENDAR_FILE = "data/calendar.json"

def add_event(title, date, time=None, description=""):
    """Add an event to the user's calendar."""
    os.makedirs("data", exist_ok=True)
    events = load_events()

    new_event = {
        "title": title,
        "date": date,
        "time": time or "00:00",
        "description": description
    }
    events.append(new_event)
    save_events(events)
    return f"📆 Event '{title}' added on {date} at {time or 'unspecified time'}."

def load_events():
    """Load events from JSON."""
    if os.path.exists(CALENDAR_FILE):
        with open(CALENDAR_FILE, "r") as f:
            return json.load(f)
    return []

def save_events(events):
    """Save all events."""
    with open(CALENDAR_FILE, "w") as f:
        json.dump(events, f, indent=4)

def get_upcoming_events(days=7):
    """Return upcoming events within next N days."""
    today = datetime.date.today()
    upcoming = []
    events = load_events()
    for e in events:
        event_date = datetime.datetime.strptime(e["date"], "%Y-%m-%d").date()
        if 0 <= (event_date - today).days <= days:
            upcoming.append(e)
    return upcoming
