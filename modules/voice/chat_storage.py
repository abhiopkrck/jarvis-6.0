import json
import os
from datetime import datetime

CHAT_FILE = r"C:\Users\Abhishek\Downloads\jarvis\modules\data\chat_history.json"

def load_chats():
    """Load chat history with proper encoding handling"""
    if not os.path.exists(CHAT_FILE):
        return []
    
    try:
        # Try UTF-8 first
        with open(CHAT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except UnicodeDecodeError:
        try:
            # Try Latin-1 as fallback
            with open(CHAT_FILE, 'r', encoding='latin-1') as f:
                return json.load(f)
        except:
            # If both fail, return empty list and create new file
            print("[⚠️] Chat file corrupted, creating new one...")
            save_chats([])
            return []
    except json.JSONDecodeError:
        # If JSON is invalid, return empty list
        print("[⚠️] Invalid JSON in chat file, creating new one...")
        save_chats([])
        return []

def save_chats(chats):
    """Save chat history with UTF-8 encoding"""
    try:
        os.makedirs(os.path.dirname(CHAT_FILE), exist_ok=True)
        with open(CHAT_FILE, 'w', encoding='utf-8') as f:
            json.dump(chats, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[❌] Error saving chats: {e}")

def log_chat(username, user_input, jarvis_response):
    """Log chat conversation with proper error handling"""
    try:
        chats = load_chats()
        
        chat_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_input,
            "jarvis": jarvis_response
        }
        
        chats.append(chat_entry)
        save_chats(chats)
        print(f"[💾] Chat saved to {CHAT_FILE}")
        
    except Exception as e:
        print(f"[❌] Error logging chat: {e}")