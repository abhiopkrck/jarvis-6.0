import json
from pathlib import Path
from datetime import datetime
import time

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "modules" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

REMINDERS_FILE = DATA_DIR / "reminders.json"

def load_reminders():
    if REMINDERS_FILE.exists():
        try:
            data = json.load(open(REMINDERS_FILE, "r"))
            if isinstance(data, list):
                return {}
            return data
        except json.JSONDecodeError:
            # Empty or invalid file → return empty dict
            return {}
    return {}

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=4)

def add_reminder(user_name, reminder_text, reminder_time):
    reminders = load_reminders()
    if not isinstance(reminders, dict):
        reminders = {}
    if user_name not in reminders:
        reminders[user_name] = []
    reminders[user_name].append({
        "reminder": reminder_text,
        "reminder_time": str(reminder_time),
        "status": "pending"
    })
    save_reminders(reminders)

def get_pending_reminders(user_name):
    reminders = load_reminders()
    if not isinstance(reminders, dict):
        return []
    return [r for r in reminders.get(user_name, []) if r["status"] == "pending"]

def mark_reminder_done(user_name, index):
    reminders = load_reminders()
    if not isinstance(reminders, dict):
        return
    if user_name in reminders and index < len(reminders[user_name]):
        reminders[user_name][index]["status"] = "done"
        save_reminders(reminders)
def reminder_loop():
    """
    Continuously check reminders for all users and notify.
    """
    while True:
        reminders = load_reminders()
        now = datetime.now()
        for user, rem_list in reminders.items():
            for idx, rem in enumerate(rem_list):
                rem_time = datetime.fromisoformat(rem["reminder_time"])
                if rem["status"] == "pending" and rem_time <= now:
                    print(f"[Reminder] {user}: {rem['reminder']}")
                    # Mark as done
                    reminders[user][idx]["status"] = "done"
        save_reminders(reminders)
        time.sleep(10)