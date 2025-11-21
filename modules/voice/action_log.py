import json
from pathlib import Path
from datetime import datetime

ACTIONS_FILE = Path("modules/data/actions.json")
ACTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)

# Load existing actions
if ACTIONS_FILE.exists():
    with open(ACTIONS_FILE, "r") as f:
        actions = json.load(f)
else:
    actions = []

def log_action(user_name, action_type, details=""):
    """Save an action performed by the user."""
    actions.append({
        "user": user_name,
        "action": action_type,
        "details": details,
        "timestamp": str(datetime.now())
    })
    save_actions()

def save_actions():
    with open(ACTIONS_FILE, "w") as f:
        json.dump(actions, f, indent=4)

def load_actions():
    return actions
