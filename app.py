import asyncio
import threading
import os
import time
from datetime import datetime
import json
import pygame
import eel
import sys
import webbrowser
import subprocess
import threading
from modules.voice.wake_word import listen_for_wake_word
from modules.voice.voice_auth import authenticate_user
from modules.voice.tts import speak
from modules.voice.reminders import reminder_loop, add_reminder
from modules.dev_tools.vscode import HuggingChatbot, ask_jarvis
from modules.voice.voice_commands import execute_command
from modules.entertainment.art_creator import generate_image,model
  # your file-processing code

# Initialize pygame mixer
pygame.mixer.init()

# Chatbot instance
chatbot = HuggingChatbot()
username = "Abhishek"
is_speaking = False
chat_history_lock = threading.Lock()

# Eel init
eel.init('web')


@eel.expose
def py_generate_image(prompt: str):
    """
    Generate an image using Bytez and open it directly in default browser.
    Returns the image URL for frontend display.
    """
    if not prompt:
        return None
    try:
        result = model.run(prompt)  # Bytez SDK returns Response object
        if result and hasattr(result, "output") and result.output:
            image_url = result.output
            webbrowser.open(image_url)  # Open image directly
            return image_url
        else:
            return None
    except Exception as e:
        print(f"[Image Generation Error] {e}")
        return None


# =========================
# SETTINGS MODULE
# =========================
DATA_FOLDER = os.path.join(os.getcwd(), "modules","system")
os.makedirs(DATA_FOLDER, exist_ok=True)

APP_FILE = os.path.join(DATA_FOLDER, "apps.json")
WEB_FILE = os.path.join(DATA_FOLDER, "websites.json")
CONTACT_FILE = os.path.join(DATA_FOLDER, "contact.json")

for file in [APP_FILE, WEB_FILE, CONTACT_FILE]:
    if not os.path.exists(file):
        with open(file, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2)

def save_to_json(file_path, new_entry):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data.append(new_entry)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        return False

@eel.expose
def add_app(name, path):
    return save_to_json(APP_FILE, {"name": name, "path": path})

@eel.expose
def add_web(name, url):
    return save_to_json(WEB_FILE, {"name": name, "url": url})

@eel.expose
def add_contact(name, phone):
    return save_to_json(CONTACT_FILE, {"name": name, "phone": phone})

@eel.expose
def get_entries(entry_type):
    file_map = {"app": APP_FILE, "web": WEB_FILE, "contact": CONTACT_FILE}
    try:
        with open(file_map[entry_type], 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# -------- Helpers --------
def safe_log_chat(user_input, response):
    try:
        from modules.voice.chat_storage import log_chat
        log_chat(username, user_input, response)
    except Exception as e:
        print(f"[❌] Chat logging error: {e}")

def speak_with_stop(text):
    global is_speaking
    if not text:
        return
    is_speaking = True
    def _speak():
        global is_speaking
        try:
            speak(text)
        except Exception as e:
            print(f"Speech error: {e}")
        finally:
            is_speaking = False
            try:
                eel.on_speaking_finished()
            except:
                pass
    threading.Thread(target=_speak, daemon=True).start()

def stop_speech():
    global is_speaking
    if is_speaking:
        try:
            pygame.mixer.music.stop()
        except:
            pass
        is_speaking = False
        return True
    return False

def open_notepad_safe():
    try:
        notepad_path = r"C:\Users\Abhishek\Downloads\jarvis\modules\data\chat_notepad.txt"
        if os.path.exists(notepad_path):
            if os.name == 'nt':
                os.startfile(notepad_path)
            else:
                import subprocess
                subprocess.run(['xdg-open', notepad_path])
            return True
        return False
    except Exception as e:
        print(f"Error opening logs: {e}")
        return False

# -------- Wake word & voice command --------
wake_word_active = False

def wake_word_loop():
    """Continuously listen for wake word after activation."""
    global wake_word_active
    while wake_word_active:
        try:
            if listen_for_wake_word():
                print("✅ Wake word detected! Listening for command...")
                speak("yes how can i help you")
                # Run execute_command safely in new event loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(execute_command())
        except Exception as e:
            print(f"[Wake Word Error] {e}")
     

@eel.expose
def py_activate_voice_mode():
    """Activate wake word detection when user clicks the Voice Mode button."""
    global wake_word_active
    if not wake_word_active:
        wake_word_active = True
        threading.Thread(target=wake_word_loop, daemon=True).start()
        print("🎤 Voice Mode activated: Listening for wake word")
        speak("voice mode activated")
        return {"ok": True, "message": "Voice Mode activated"}
    else:
        return {"ok": False, "message": "Voice Mode already active"}

@eel.expose
def py_stop_voice_mode():
    global wake_word_active
    wake_word_active = False
    print("🛑 Voice Mode deactivated")
    speak("voice mode dactivated")
    return {"ok": True, "message": "Voice Mode deactivated"}

# -------- Eel exposed chat functions --------
@eel.expose
def py_send_query(query):
    global chatbot
    if not query:
        return {"ok": False, "error": "Empty query"}
    try:
        response = chatbot.get_response(query)
        safe_log_chat(query, response)
        speak_with_stop(response)
        ts = datetime.now().strftime("%H:%M:%S")
        return {"ok": True, "response": response, "timestamp": ts}
    except Exception as e:
        print(f"[py_send_query error] {e}")
        return {"ok": False, "error": str(e)}
@eel.expose
def jarvis_intro():
    """Play Jarvis voice intro after video ends"""
    def _speak():
        speak("Initializing systems. Welcome, Abhishek.")
    threading.Thread(target=_speak, daemon=True).start()
@eel.expose
def py_stop_speech():
    return {"stopped": stop_speech()}

@eel.expose
def py_clear_chat():
    return {"ok": True}

@eel.expose
def py_open_logs():
    return {"ok": open_notepad_safe()}

@eel.expose
def py_exit_app():
    """Exit Jarvis completely"""
    try:
        # Stop pygame
        pygame.mixer.quit()
    except:
        pass

    # Close frontend
    try:
        # Attempt to terminate Chrome window started by Eel
        if sys.platform == "win32":
            subprocess.call(["taskkill", "/F", "/IM", "chrome.exe"])
        else:
            # For Linux / Mac
            subprocess.call(["pkill", "-f", "chrome"])
    except Exception as e:
        print(f"Error closing browser: {e}")

    # Stop backend
    os._exit(0)
@eel.expose
def py_get_time():
    now = datetime.now()
    return {
        "date": now.strftime("%d %b %Y"),
        "time": now.strftime("%I:%M:%S %p"),
        "day": now.strftime("%A")
    }

# -------- Background reminder loop --------
def start_reminder_loop():
    threading.Thread(target=reminder_loop, daemon=True).start()

# -------- Program entry --------
if __name__ == "__main__":
    start_reminder_loop()
    eel.start('index.html', size=(700, 650))
