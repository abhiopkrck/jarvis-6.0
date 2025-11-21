import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "modules" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

USERS_FILE = DATA_DIR / "users.json"

def load_users():
    if USERS_FILE.exists():
        data = json.load(open(USERS_FILE, "r"))
        if isinstance(data, list):
            return {u["name"]: u for u in data if "name" in u}
        return data
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def add_user(name, voice_profile=None):
    users = load_users()
    if name not in users:
        users[name] = {"voice_profile": voice_profile}
    save_users(users)
    return name

def get_user(name):
    return load_users().get(name)

def update_user_voice_profile(name, voice_profile):
    users = load_users()
    if name in users:
        users[name]["voice_profile"] = voice_profile
    save_users(users)
