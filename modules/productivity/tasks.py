import json
import os

TASKS_FILE = "data/tasks.json"

def add_task(task, priority="medium"):
    """Add a new task."""
    os.makedirs("data", exist_ok=True)
    tasks = load_tasks()
    tasks.append({"task": task, "priority": priority, "done": False})
    save_tasks(tasks)
    return f"✅ Task added: {task}"

def mark_done(index):
    """Mark a task as completed."""
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks(tasks)
        return f"🎉 Task '{tasks[index]['task']}' marked done!"
    return "⚠️ Invalid task index."

def list_tasks(show_all=True):
    """List all tasks."""
    tasks = load_tasks()
    if not show_all:
        tasks = [t for t in tasks if not t["done"]]
    return tasks

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)
