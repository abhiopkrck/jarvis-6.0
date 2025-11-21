import os
import json
import asyncio
import webbrowser

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build paths to JSON files
APPS_FILE = os.path.join(BASE_DIR, "apps.json")
WEBSITES_FILE = os.path.join(BASE_DIR, "websites.json")

# Load apps from JSON
try:
    with open(APPS_FILE, "r") as f:
        apps_list = json.load(f)
        # Convert list to dict: name (lowercase) -> path
        apps = {app["name"].lower(): os.path.expandvars(app["path"]) for app in apps_list}
except FileNotFoundError:
    print(f"[Error] apps.json not found at {APPS_FILE}")
    apps = {}

# Load websites from JSON
try:
    with open(WEBSITES_FILE, "r") as f:
        websites_list = json.load(f)
        # Convert list to dict: name (lowercase) -> url
        websites = {site["name"].lower(): site["url"] for site in websites_list}
except FileNotFoundError:
    print(f"[Error] websites.json not found at {WEBSITES_FILE}")
    websites = {}

async def launch_app(app_name: str):
    """
    Launch an app or open a website.
    """
    name_lower = app_name.lower()

    # Check if it's an installed app
    path = apps.get(name_lower)
    if path and os.path.exists(path):
        os.startfile(path)
        await asyncio.sleep(1)
        print(f"[System] Launched {app_name}")
    
    # Check if it's a known website
    elif name_lower in websites:
        url = websites[name_lower]
        webbrowser.open(url)
        await asyncio.sleep(1)
        print(f"[System] Opened website: {url}")
    
    # Check if it's a direct URL
    elif app_name.startswith("http://") or app_name.startswith("https://"):
        webbrowser.open(app_name)
        await asyncio.sleep(1)
        print(f"[System] Opened website: {app_name}")
    
    else:
        print(f"[System] App or website '{app_name}' not found")

# Example usage
if __name__ == "__main__":
    app_to_launch = input("Enter app or website name: ")
    asyncio.run(launch_app(app_to_launch))
