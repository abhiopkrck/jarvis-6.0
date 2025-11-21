import os
import re
import json
from datetime import datetime
import eel

# ---------- Bytez / Google Gemini ONLY (LM Studio Removed) ----------
from bytez import Bytez
BYTEZ_API_KEY = "your api key"
sdk = Bytez(BYTEZ_API_KEY)
GEMINI_MODEL = sdk.model("google/gemini-2.5-flash")

def ask_with_history(chat_history):
    try:
        result = GEMINI_MODEL.run(chat_history)
    except Exception as e:
        return False, f"Error calling Gemini: {e}"

    if getattr(result, "error", None):
        return False, str(result.error)

    output = result.output
    if isinstance(output, dict) and "content" in output:
        return True, output["content"]
    if isinstance(output, list) and len(output)>0 and isinstance(output[0], dict) and "content" in output[0]:
        return True, output[0]["content"]

    return True, str(output)

# ---------------------------------------------------

@eel.expose
def ask_jarvis(prompt):
    chat_history = [
        {"role": "system", "content": "You are Jarvis, a smart, polite, assistant."},
        {"role": "user", "content": prompt}
    ]
    success, reply = ask_with_history(chat_history)
    return reply if success else f"❌ Gemini Error: {reply}"

# ---------------------------------------------------
# 🚫 HuggingChatbot REMOVED (LM Studio removed)
# ---------------------------------------------------

class HuggingChatbot:
    """Jarvis Chatbot powered ONLY by Gemini"""
    def __init__(
        self,
        history_path=r"C:\Users\Abhishek\Downloads\jarvis\modules\data\chat_history.json",
        notepad_path=r"C:\Users\Abhishek\Downloads\jarvis\modules\data\chat_notepad.txt"
    ):
        print("[+] Initializing Jarvis (Gemini ONLY mode enabled)...")
        self.history_path = history_path
        self.notepad_path = notepad_path

        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.notepad_path), exist_ok=True)
        self._initialize_files()

    def _initialize_files(self):
        if not os.path.exists(self.notepad_path):
            with open(self.notepad_path, "w", encoding="utf-8") as f:
                f.write("🤖 Jarvis AI Chat Log\n" + "="*50 + "\n")
                f.write(f"Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        if not os.path.exists(self.history_path):
            with open(self.history_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)

    def get_response(self, prompt):
        reply = ask_jarvis(prompt)
        clean_reply = re.sub(r"[#@^%*_=~<>\\/\[\]{}|]", "", reply)
        self._save_to_history(prompt, clean_reply)
        self._save_to_notepad(prompt, clean_reply)
        return clean_reply

    def _save_to_history(self, user_input, response):
        try:
            if os.path.exists(self.history_path):
                with open(self.history_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = []

            data.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user": user_input,
                "jarvis": response
            })

            with open(self.history_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"[⚠️] History Save Error: {e}")

    def _save_to_notepad(self, user_input, response):
        try:
            with open(self.notepad_path, "a", encoding="utf-8") as f:
                f.write(f"\n🧑 You: {user_input}\n🤖 Jarvis: {response}\n")
        except Exception as e:
            print(f"[⚠️] Notepad Save Error: {e}")
