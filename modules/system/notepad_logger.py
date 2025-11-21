import pyautogui, time, threading, os

class NoteLogger:
    def __init__(self):
        self.notepad_open = False
        self.lock = threading.Lock()

    def open_notepad(self):
        with self.lock:
            if not self.notepad_open:
                pyautogui.hotkey("win", "r")
                time.sleep(1)
                pyautogui.write("notepad")
                pyautogui.press("enter")
                time.sleep(1.5)
                self.notepad_open = True
                pyautogui.write("==== JARVIS CHAT LOG ====\n\n")

    def log(self, user_text, bot_text):
        self.open_notepad()
        time.sleep(0.1)
        pyautogui.write(f"User: {user_text}\n")
        pyautogui.write(f"Jarvis: {bot_text}\n")
        pyautogui.write("---------------\n")
