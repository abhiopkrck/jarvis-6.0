import os
import re
import json
import subprocess
from datetime import datetime
from hugchat import hugchat

# ✅ Optional TTS import
try:
    from modules.voice.tts import speak
except ImportError:
    def speak(text):
        print("[Voice Disabled] " + text)


class HuggingChatbot:
    def __init__(
        self,
        cookie_path=r"C:\Users\Abhishek\Downloads\jarvis\modules\internet\cookies.json",
        history_path=r"C:\Users\Abhishek\Downloads\jarvis\modules\data\chat_history.json",
        notepad_path=r"C:\Users\Abhishek\Downloads\jarvis\modules\data\chat_notepad.txt"
    ):
        print("[+] Initializing HuggingChat chatbot...")
        self.cookie_path = cookie_path
        self.history_path = history_path
        self.notepad_path = notepad_path
        self.chatbot = self._load_chatbot()
        self.current_conversation = self.chatbot.new_conversation()
        self.chatbot.change_conversation(self.current_conversation)

        # ✅ Ensure chat history file exists with proper structure
        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
        self._initialize_history_file()

        # ✅ Ensure notepad file exists
        os.makedirs(os.path.dirname(self.notepad_path), exist_ok=True)
        if not os.path.exists(self.notepad_path):
            with open(self.notepad_path, "w", encoding="utf-8") as f:
                f.write("🤖 Jarvis AI Chat Log\n")
                f.write("=" * 50 + "\n")
                f.write(f"Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")

    def _load_chatbot(self):
        """Load HuggingChat chatbot using cookies."""
        if not os.path.exists(self.cookie_path):
            print("[!] Cookie file missing. Cannot proceed without login!")
            raise FileNotFoundError(f"Cookie file not found: {self.cookie_path}")
        return hugchat.ChatBot(cookie_path=self.cookie_path)

    def _initialize_history_file(self):
        """Initialize chat history file with proper list structure."""
        try:
            if not os.path.exists(self.history_path):
                with open(self.history_path, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4, ensure_ascii=False)
            else:
                # Check if file has valid list structure
                with open(self.history_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if not content:
                        # Empty file, initialize with list
                        with open(self.history_path, "w", encoding="utf-8") as f:
                            json.dump([], f, indent=4, ensure_ascii=False)
                    else:
                        data = json.loads(content)
                        if not isinstance(data, list):
                            # Convert dictionary to list or create new list
                            print("[⚠️] Chat history was a dictionary, converting to list...")
                            with open(self.history_path, "w", encoding="utf-8") as f:
                                json.dump([], f, indent=4, ensure_ascii=False)
        except (json.JSONDecodeError, Exception) as e:
            print(f"[⚠️] Error initializing history file: {e}. Creating new one...")
            with open(self.history_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)

    def _clean_text(self, text: str) -> str:
        """Clean unwanted special characters for speech."""
        # Remove unwanted characters but keep sentence structure
        text = re.sub(r"[#@^%*_=~<>\\/\[\]{}|]", "", text)
        text = re.sub(r"\s+", " ", text).strip()  # normalize spacing
        return text

    def _save_to_history(self, user_input, response_text):
        """Save user and bot messages to chat_history.json."""
        try:
            # Load old history safely with error handling
            history = []
            if os.path.exists(self.history_path):
                try:
                    with open(self.history_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:
                            data = json.loads(content)
                            if isinstance(data, list):
                                history = data
                            else:
                                print("[⚠️] History was not a list, starting fresh...")
                                history = []
                except (json.JSONDecodeError, Exception) as e:
                    print(f"[⚠️] Error reading history file: {e}. Starting fresh...")
                    history = []

            # ✅ Add new entry (always at end)
            entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user": user_input,
                "jarvis": response_text
            }
            history.append(entry)

            # ✅ Save updated history (chronological order)
            with open(self.history_path, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=4, ensure_ascii=False)

            print(f"[💾 Chat saved → {self.history_path}]")

        except Exception as e:
            print(f"[⚠️ Error saving chat history]: {e}")

    def _write_to_notepad(self, user_input, response_text):
        """Write conversation to notepad file."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.notepad_path, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}]\n")
                f.write(f"👤 You: {user_input}\n")
                f.write(f"🤖 Jarvis: {response_text}\n")
                f.write("-" * 80 + "\n\n")
            
            print(f"[📝 Notepad updated → {self.notepad_path}]")
            
        except Exception as e:
            print(f"[⚠️ Error writing to notepad]: {e}")

    def _open_notepad(self):
        """Open the notepad file in default text editor."""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.notepad_path)
            elif os.name == 'posix':  # macOS or Linux
                if os.uname().sysname == 'Darwin':  # macOS
                    subprocess.run(['open', self.notepad_path])
                else:  # Linux
                    subprocess.run(['xdg-open', self.notepad_path])
            else:
                print(f"[ℹ️] Notepad file location: {self.notepad_path}")
            
            print(f"[📖 Opened notepad file: {self.notepad_path}]")
            return True
            
        except Exception as e:
            print(f"[⚠️ Error opening notepad]: {e}")
            print(f"[ℹ️] You can manually open: {self.notepad_path}")
            return False

    def get_response(self, query: str, auto_open_notepad=True):
        """Send query to HuggingChat and log to notepad."""
        try:
            query = query.strip()
            if not query:
                return "No input received."

            response = self.chatbot.chat(query)
            response_text = response.text.strip() if hasattr(response, "text") else str(response).strip()

            clean_response = self._clean_text(response_text)

            print(f"[🤖 Jarvis AI]: {response_text}")

            # ✅ Save to history file
            self._save_to_history(query, response_text)

            # ✅ Write to Notepad
            self._write_to_notepad(query, response_text)

            # ✅ Auto-open notepad file after response
            if auto_open_notepad:
                self._open_notepad()

            return response_text

        except Exception as e:
            print(f"[Chatbot Error] {e}")
            return "Sorry, there was a problem with the chatbot."

    def clear_notepad(self):
        """Clear the notepad file and start fresh."""
        try:
            with open(self.notepad_path, "w", encoding="utf-8") as f:
                f.write("🤖 Jarvis AI Chat Log\n")
                f.write("=" * 50 + "\n")
                f.write(f"Cleared on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
            print(f"[🗑️ Notepad cleared → {self.notepad_path}]")
            
            # Auto-open the cleared notepad
            self._open_notepad()
            
            return "Notepad cleared successfully!"
        except Exception as e:
            print(f"[⚠️ Error clearing notepad]: {e}")
            return "Error clearing notepad."

    def read_notepad(self):
        """Read the entire notepad content."""
        try:
            with open(self.notepad_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"[⚠️ Error reading notepad]: {e}")
            return "Error reading notepad."

    def open_notepad_file(self):
        """Manually open the notepad file."""
        return self._open_notepad()

    def clear_history(self):
        """Clear the chat history file."""
        try:
            with open(self.history_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)
            print(f"[🗑️ History cleared → {self.history_path}]")
            return "Chat history cleared successfully!"
        except Exception as e:
            print(f"[⚠️ Error clearing history]: {e}")
            return "Error clearing chat history."


# Example usage
if __name__ == "__main__":
    # Initialize chatbot
    chatbot = HuggingChatbot()
    
    # Example conversation
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        elif user_input.lower() == 'clear notepad':
            result = chatbot.clear_notepad()
            print(result)
        elif user_input.lower() == 'clear history':
            result = chatbot.clear_history()
            print(result)
        elif user_input.lower() == 'read notepad':
            content = chatbot.read_notepad()
            print("\n" + "="*50)
            print("Notepad Content:")
            print("="*50)
            print(content)
        elif user_input.lower() == 'open notepad':
            chatbot.open_notepad_file()
        else:
            # Get response with auto-notepad opening
            response = chatbot.get_response(user_input, auto_open_notepad=True)
            print(f"🤖 Jarvis: {response}")