import os
import json
import webbrowser
import urllib.parse
import pyautogui
import time

# ✅ Persistent contacts file
CONTACTS_FILE = "system/contact.json"

# ✅ Default built-in contacts (these always exist)
DEFAULT_CONTACTS = {
    "abhishek": "abhishekboyaneco23859@gmail.com",
    "om": "omchavan0404@gmail.com",
    "yash": "yashbhosle0609@gmail.com",
    "manager": "boss@company.com"
}

# 🧠 Load contacts from file (merging defaults + saved)
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, "r") as f:
                saved = json.load(f)
            # Merge — saved contacts override defaults
            contacts = {**DEFAULT_CONTACTS, **saved}
            return contacts
        except json.JSONDecodeError:
            return DEFAULT_CONTACTS
    else:
        return DEFAULT_CONTACTS


def save_contacts(contacts):
    """Save only non-default contacts (user-added)."""
    os.makedirs("data", exist_ok=True)
    user_added = {
        name: email for name, email in contacts.items()
        if name not in DEFAULT_CONTACTS
    }
    with open(CONTACTS_FILE, "w") as f:
        json.dump(user_added, f, indent=4)


def add_contact(name, email):
    """Add contact permanently (saves to JSON + memory)."""
    contacts = load_contacts()
    contacts[name.lower()] = email
    save_contacts(contacts)
    return f"📇 Contact '{name}' saved permanently."


def find_contact(name):
    """Find a contact by name or partial match."""
    contacts = load_contacts()
    name = name.lower()
    if name in contacts:
        return contacts[name]
    for key, val in contacts.items():
        if name in key:
            return val
    return None


def send_email_gmail(name, subject, body):
    """Open Gmail compose with pre-filled fields (no login, no password)."""
    receiver = find_contact(name)
    if not receiver:
        return f"⚠️ No email found for '{name}'. Try adding it first."

    # URL encode
    subject_encoded = urllib.parse.quote(subject)
    body_encoded = urllib.parse.quote(body)

    gmail_url = (
        f"https://mail.google.com/mail/?view=cm&fs=1"
        f"&to={receiver}&su={subject_encoded}&body={body_encoded}"
    )

    # 🌐 Open Gmail (auto-login if Chrome is logged in)
    webbrowser.get("windows-default").open(gmail_url)

    # 🕒 Wait & auto-send
    time.sleep(8)  # Adjust delay for your internet
    pyautogui.hotkey('ctrl', 'enter')  # Gmail send shortcut
    time.sleep(1)

    return f"📤 Email sent automatically to {name.title()} ({receiver})!"
