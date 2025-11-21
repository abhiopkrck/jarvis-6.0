import json
from pathlib import Path

USERS_FILE = Path("modules/voice/users.json")
USERS_FILE.parent.mkdir(parents=True, exist_ok=True)

# ---------------- Safe JSON Load/Save ----------------
def load_users():
    if not USERS_FILE.exists():
        return []
    try:
        with open(USERS_FILE, "r") as f:
            data = f.read().strip()
            return json.loads(data) if data else []
    except json.JSONDecodeError:
        return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------------- Authentication (auto-login) ----------------
def authenticate_user():
    users = load_users()

    # If no users exist, create a default user
    if not users:
        default_user = {"username": "default_user", "voice_profile": "default"}
        users.append(default_user)
        save_users(users)
        print(f"[Voice Auth] No users found. Default user created: {default_user['username']}")
        return default_user['username']

    # Otherwise, use the first user in the list
    user = users[0]
    print(f"[Voice Auth] Auto-login as {user.get('username', 'default_user')}")
    return user.get("username", "default_user")

# ---------------- Add user manually ----------------
def add_user(username, voice_profile="default"):
    users = load_users()
    for user in users:
        if user.get("username", "").lower() == username.lower():
            print(f"[Voice Auth] User {username} already exists.")
            return
    users.append({"username": username, "voice_profile": voice_profile})
    save_users(users)
    print(f"[Voice Auth] User {username} added.")
