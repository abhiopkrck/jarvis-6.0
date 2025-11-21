import asyncio
import threading
import os
import time
import tkinter as tk
from datetime import datetime
import pygame  # Added for audio control

# ====== MODULE IMPORTS ====== #
from modules.voice.wake_word import listen_for_wake_word
from modules.voice.voice_auth import authenticate_user
from modules.voice.tts import speak
from modules.voice.reminders import reminder_loop
from modules.dev_tools.vscode import HuggingChatbot,ask_jarvis

# ====== GLOBAL VARIABLES ====== #
chatbot = HuggingChatbot()
username = "Abhishek"
is_speaking = False  # Global flag to track if Jarvis is speaking
pygame.mixer.init()  # Initialize pygame mixer for audio control

# ====== UI CLASS WITH REAL-TIME CLOCK ====== #
class JarvisUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS Assistant - AI Personal Assistant")
        self.root.geometry("700x650")  # Increased height for new button
        self.root.configure(bg='#1e1e1e')
        
        # Set window icon (optional)
        try:
            self.root.iconbitmap("jarvis_icon.ico")  # Add your icon file
        except:
            pass
        
        self.setup_ui()
        self.start_clock()
        
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#1e1e1e')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ====== HEADER WITH REAL-TIME CLOCK ====== #
        header_frame = tk.Frame(main_container, bg='#2d2d2d', relief=tk.RAISED, bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Left side - Title
        title_label = tk.Label(
            header_frame,
            text="🤖 JARVIS AI ASSISTANT",
            font=("Arial", 16, "bold"),
            fg="#00ff00",
            bg="#2d2d2d"
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Right side - Real-time clock
        clock_frame = tk.Frame(header_frame, bg="#2d2d2d")
        clock_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Date display
        self.date_label = tk.Label(
            clock_frame,
            text="",
            font=("Arial", 10, "bold"),
            fg="#ffffff",
            bg="#2d2d2d"
        )
        self.date_label.pack(anchor=tk.E)
        
        # Time display
        self.time_label = tk.Label(
            clock_frame,
            text="",
            font=("Arial", 12, "bold"),
            fg="#00ff00",
            bg="#2d2d2d"
        )
        self.time_label.pack(anchor=tk.E)
        
        # Day display
        self.day_label = tk.Label(
            clock_frame,
            text="",
            font=("Arial", 9),
            fg="#cccccc",
            bg="#2d2d2d"
        )
        self.day_label.pack(anchor=tk.E)
        
        # ====== STATUS BAR ====== #
        status_frame = tk.Frame(main_container, bg='#2d2d2d', relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = tk.Label(
            status_frame,
            text="🔹 System: Ready | Voice: Active | AI: Online",
            font=("Arial", 10),
            fg="#00ff00",
            bg="#2d2d2d",
            pady=5
        )
        self.status_label.pack()
        
        # ====== CHAT DISPLAY FRAME ====== #
        chat_container = tk.Frame(main_container, bg='#1e1e1e')
        chat_container.pack(fill=tk.BOTH, expand=True)
        
        # Chat header
        chat_header = tk.Label(
            chat_container,
            text="💬 CONVERSATION",
            font=("Arial", 12, "bold"),
            fg="#00ff00",
            bg="#1e1e1e"
        )
        chat_header.pack(anchor=tk.W, pady=(0, 5))
        
        chat_display_frame = tk.Frame(chat_container, bg="#2d2d2d", relief=tk.SUNKEN, bd=1)
        chat_display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for chat
        scrollbar = tk.Scrollbar(chat_display_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Chat Text Area
        self.chat_display = tk.Text(
            chat_display_frame,
            height=15,
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Arial", 20),
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chat_display.yview)
        
        # Configure text colors
        self.chat_display.tag_configure("user", foreground="#00ff00")
        self.chat_display.tag_configure("jarvis", foreground="#007acc")
        self.chat_display.tag_configure("system", foreground="#ffa500")
        
        # ====== INPUT FRAME ====== #
        input_frame = tk.Frame(main_container, bg="#1e1e1e")
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Input Label
        input_label = tk.Label(
            input_frame,
            text="Enter your command:",
            font=("Arial", 10, "bold"),
            fg="#ffffff",
            bg="#1e1e1e"
        )
        input_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Input Entry Box
        input_entry_frame = tk.Frame(input_frame, bg="#3d3d3d", relief=tk.SUNKEN, bd=1)
        input_entry_frame.pack(fill=tk.X)
        
        self.input_entry = tk.Entry(
            input_entry_frame,
            font=("Arial", 20),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT
        )
        self.input_entry.pack(fill=tk.X, padx=2, pady=2)
        self.input_entry.bind("<Return>", self.send_query)
        
        # ====== BUTTONS FRAME ====== #
        button_frame = tk.Frame(main_container, bg="#1e1e1e")
        button_frame.pack(fill=tk.X, pady=10)
        
        # Button styles
        button_style = {
            "font": ("Arial", 10),
            "padx": 15,
            "pady": 8
        }
        
    
  
        # EMERGENCY STOP SPEECH BUTTON (ONLY STOPS SPEECH, NOT JARVIS)
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️ STOP Speech",
            command=self.stop_speech_only,
            bg="#ff0000",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear Button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear Chat",
            command=self.clear_chat,
            bg="#d9534f",
            fg="#ffffff",
            **button_style
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Notepad Button
        notepad_btn = tk.Button(
            button_frame,
            text="📝 Open Logs",
            command=self.open_notepad_safe,
            bg="#ffa500",
            fg="#ffffff",
            **button_style
        )
        notepad_btn.pack(side=tk.LEFT, padx=5)
        
        # Exit Button (Separate - Only this closes Jarvis)
        exit_btn = tk.Button(
            button_frame,
            text="🔴 Exit Jarvis",
            command=self.exit_app,
            bg="#8B0000",
            fg="#ffffff",
            **button_style
        )
        exit_btn.pack(side=tk.LEFT, padx=5)
        
        # Focus on input entry
        self.input_entry.focus()
        
    def start_clock(self):
        """Start real-time clock updates"""
        self.update_clock()
        
    def update_clock(self):
        """Update the real-time clock display"""
        now = datetime.now()
        
        # Update date (e.g., "02 Nov 2024")
        date_str = now.strftime("%d %b %Y")
        self.date_label.config(text=date_str)
        
        # Update time (e.g., "02:30:45 PM")
        time_str = now.strftime("%I:%M:%S %p")
        self.time_label.config(text=time_str)
        
        # Update day (e.g., "Saturday")
        day_str = now.strftime("%A")
        self.day_label.config(text=day_str)
        
        # Update every second
        self.root.after(1000, self.update_clock)
        
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=f"🔹 {message}")
        
    def add_to_chat(self, sender, message):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if sender == "You":
            tag = "user"
            prefix = "👤 You:"
        elif sender == "Jarvis":
            tag = "jarvis"
            prefix = "🤖 Jarvis:"
        else:
            tag = "system"
            prefix = "⚡ System:"
            
        self.chat_display.insert(tk.END, f"[{timestamp}] {prefix}\n", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.see(tk.END)
        
    def send_query(self, event=None):
        """Send query to HuggingChat and get response"""
        query = self.input_entry.get().strip()
        if not query:
            return
            
        # Clear input field
        self.input_entry.delete(0, tk.END)
        
        # Add user message to chat
        self.add_to_chat("You", query)
        self.update_status("Processing your command...")
        
        # Process in a separate thread to avoid UI freeze
        threading.Thread(target=self.process_query, args=(query,), daemon=True).start()
        
    def process_query(self, query):
        """Process query with HuggingChat (run in thread)"""
        try:
            # Get response from HuggingChat
            response = chatbot.get_response(query)
            
            # Manually open notepad after getting response
            # self.open_notepad_safe()
            
            # Update UI in main thread
            self.root.after(0, lambda: self.add_to_chat("Jarvis", response))
            self.root.after(0, lambda: self.update_status("Ready | Command executed"))
            
            # ✅ FIXED: Use safe chat logging
            self.root.after(0, lambda: self.safe_log_chat(query, response))
            
            # Speak the response with stop capability
            self.speak_with_stop(response)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.add_to_chat("Jarvis", error_msg))
            self.root.after(0, lambda: self.update_status("Error occurred"))
    
    def speak_with_stop(self, text):
        """Speak text with ability to stop"""
        global is_speaking
        is_speaking = True
        self.update_status("Jarvis Speaking... Click STOP to interrupt")
        
        # Run speech in a separate thread to avoid blocking
        def speak_thread():
            try:
                speak(text)
            except Exception as e:
                print(f"Speech error: {e}")
            finally:
                is_speaking = False
                self.root.after(0, lambda: self.update_status("Ready"))
        
        threading.Thread(target=speak_thread, daemon=True).start()
            
    def stop_speech_only(self):
        """ONLY stops Jarvis speech - does NOT close Jarvis"""
        global is_speaking
        if is_speaking:
            # Method 1: Stop pygame mixer (for any playing audio)
            try:
                pygame.mixer.music.stop()
            except:
                pass
            
            # Method 2: Kill TTS processes gently
            try:
                if os.name == 'nt':  # Windows
                    # Only kill Python processes related to TTS, not the main Jarvis
                    os.system('taskkill /f /im python.exe /t /fi "WINDOWTITLE eq TTS*" 2>nul')
                else:  # Linux/Mac
                    os.system('pkill -f "python.*tts" 2>/dev/null')
            except:
                pass
            
            # Method 3: Stop any active audio playback
            try:
                import subprocess
                if os.name == 'nt':
                    subprocess.run(['taskkill', '/f', '/im', 'wmplayer.exe'], capture_output=True)
                else:
                    subprocess.run(['pkill', 'aplay'], capture_output=True)
                    subprocess.run(['pkill', 'paplay'], capture_output=True)
            except:
                pass
            
            is_speaking = False
            self.add_to_chat("system", "🗣️ Speech stopped by user")
            self.update_status("Speech stopped | Ready")
            print("🛑 Speech stopped by user (Jarvis continues running)")
        else:
            self.add_to_chat("system", "No active speech to stop")
            self.update_status("No speech active")
            
    def safe_log_chat(self, user_input, response):
        """Safely log chat with proper encoding handling"""
        try:
            # Import here to avoid circular imports
            from modules.voice.chat_storage import log_chat
            log_chat(username, user_input, response)
        except UnicodeDecodeError:
            # If there's an encoding error, create a new chat file
            try:
                chat_file = r"C:\Users\Abhishek\Downloads\jarvis\modules\data\chat_history.json"
                # Create backup of corrupted file
                if os.path.exists(chat_file):
                    backup_file = chat_file + ".backup"
                    os.rename(chat_file, backup_file)
                    print(f"[⚠️] Chat file corrupted. Created backup: {backup_file}")
                
                # Create new chat file with UTF-8 encoding
                new_chat = [{
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "user": user_input,
                    "jarvis": response
                }]
                
                import json
                with open(chat_file, 'w', encoding='utf-8') as f:
                    json.dump(new_chat, f, indent=2, ensure_ascii=False)
                    
                print(f"[✅] Created new chat file with UTF-8 encoding")
                
            except Exception as e:
                print(f"[❌] Failed to create new chat file: {e}")
        except Exception as e:
            print(f"[❌] Chat logging error: {e}")
            
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.delete(1.0, tk.END)
        self.add_to_chat("system", "Chat history cleared")
        self.update_status("Chat cleared | Ready")
        
    def activate_voice_mode(self):
        """Activate voice command mode"""
        self.update_status("Listening for voice command... Speak now")
        self.speak_with_stop("Voice mode activated. Say 'Jarvis' to wake me up.")
        
    def open_notepad_safe(self):
        """Safely open notepad file with UTF-8 encoding"""
        try:
            notepad_path = r"C:\Users\Abhishek\Downloads\jarvis\modules\data\chat_notepad.txt"
            
            if os.path.exists(notepad_path):
                try:
                    with open(notepad_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    try:
                        with open(notepad_path, 'r', encoding='latin-1') as f:
                            content = f.read()
                    except:
                        return False
            
            if os.name == 'nt':
                os.startfile(notepad_path)
            else:
                import subprocess
                subprocess.run(['xdg-open', notepad_path])
            
            self.update_status("Notepad opened | Logs available")
            return True
            
        except Exception as e:
            self.update_status("Error opening logs")
            return False
    
    def exit_app(self):
        """Exit the application safely - ONLY this closes Jarvis"""
        global is_speaking
        is_speaking = False  # Stop any ongoing speech
        pygame.mixer.quit()  # Clean up pygame
        self.root.quit()
        self.root.destroy()
        print("🔴 JARVIS Assistant Shutting Down...")
        os._exit(0)  # Force exit all threads
            
    def run(self):
        """Start the UI"""
        self.root.mainloop()

# ====== FIXED VOICE COMMAND FUNCTION ====== #
async def fixed_execute_command(ui_instance=None):
    """Fixed version of execute_command"""
    import speech_recognition as sr
    from modules.voice.nlu import parse_command
    
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("\n🎤 Listening for your command...\n")

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("[Jarvis] Listening...")
            
            if ui_instance:
                ui_instance.root.after(0, lambda: ui_instance.update_status("Listening... Speak now"))
            
            audio = recognizer.listen(source, timeout=10)

        command_text = recognizer.recognize_google(audio)
        print(f"🧠 You said: {command_text}")

        if ui_instance:
            ui_instance.root.after(0, lambda: ui_instance.add_to_chat("You", command_text))
            ui_instance.root.after(0, lambda: ui_instance.update_status("Processing voice command..."))

        action, param = parse_command(command_text)
        command = command_text.lower()

        # Handle different commands
        if action == "open_app":
            from modules.system.app_launcher import launch_app
            reply = f"Opening {param}"
            if ui_instance:
                ui_instance.speak_with_stop(reply)
                ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", reply))
            await launch_app(param)
            if ui_instance:
                ui_instance.safe_log_chat(command_text, reply)

        elif "send email" in command:
            from modules.productivity.email_manager import send_email_gmail
            if ui_instance:
                ui_instance.speak_with_stop("Which person?")
                ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", "Which person?"))
            
            with mic as source:
                audio = recognizer.listen(source)
            name = recognizer.recognize_google(audio).lower().strip()

            if ui_instance:
                ui_instance.speak_with_stop("What is the subject of your email?")
                ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", "What is the subject of your email?"))
            
            with mic as source:
                audio = recognizer.listen(source)
            subject = recognizer.recognize_google(audio).strip()

            if ui_instance:
                ui_instance.speak_with_stop("What message would you like to send?")
                ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", "What message would you like to send?"))
            
            with mic as source:
                audio = recognizer.listen(source)
            body = recognizer.recognize_google(audio).strip()

            send_email_gmail(name, subject, body)
            reply = f"✅ Email sent to {name}"
            if ui_instance:
                ui_instance.speak_with_stop(reply)
                ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", reply))
                ui_instance.safe_log_chat(command_text, reply)

        elif action == "search_web":
            from modules.internet.web_search import search_web
            reply = f"Searching for {param}"
            if ui_instance:
                ui_instance.speak_with_stop(reply)
                ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", reply))
            await search_web(param)
            if ui_instance:
                ui_instance.safe_log_chat(command_text, reply)

        elif "play music" in command:
            from modules.entertainment.music_control import handle_music_command
            reply = "Playing music"
            if ui_instance:
                ui_instance.speak_with_stop(reply)
                ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", reply))
            await handle_music_command(command)
            if ui_instance:
                ui_instance.safe_log_chat(command_text, reply)

        elif "play" in command and "on youtube" in command:
            from modules.entertainment.video_player import play_youtube
            reply = "Playing on YouTube"
            if ui_instance:
                ui_instance.speak_with_stop(reply)
                ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", reply))
            play_youtube(command)
            if ui_instance:
                ui_instance.safe_log_chat(command_text, reply)

        elif action == "set_reminder":
            from modules.voice.reminders import add_reminder
            from datetime import timedelta
            reminder_text = param
            reminder_time = datetime.now() + timedelta(seconds=60)
            add_reminder(username, reminder_text, reminder_time)
            reply = f"Reminder set: {reminder_text}"
            if ui_instance:
                ui_instance.speak_with_stop(reply)
                ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", reply))
                ui_instance.safe_log_chat(command_text, reply)

        elif action == "take_screenshot":
            from modules.system.screenshot import take_screenshot
            reply = "Taking screenshot"
            if ui_instance:
                ui_instance.speak_with_stop(reply)
                ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", reply))
            await take_screenshot()
            if ui_instance:
                ui_instance.safe_log_chat(command_text, reply)
       
        else:
            # AI response for unknown commands
            response = chatbot.get_response(command_text)
            if ui_instance:
                ui_instance.open_notepad_safe()
                ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", response))
                ui_instance.root.after(0, lambda: ui_instance.update_status("Ready"))
                ui_instance.safe_log_chat(command_text, response)
            
            if ui_instance:
                ui_instance.speak_with_stop(response)

        return command_text

    except sr.UnknownValueError:
        error_msg = "I could not understand you. Please try again."
        if ui_instance:
            ui_instance.speak_with_stop(error_msg)
            ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", error_msg))
            ui_instance.root.after(0, lambda: ui_instance.update_status("Voice recognition failed"))
        return None
        
    except Exception as e:
        error_msg = "Voice recognition error occurred."
        if ui_instance:
            ui_instance.speak_with_stop(error_msg)
            ui_instance.root.after(0, lambda: ui_instance.add_to_chat("Jarvis", f"{error_msg} Error: {str(e)}"))
            ui_instance.root.after(0, lambda: ui_instance.update_status("Voice recognition failed"))
        return None

# ====== INITIALIZATION ====== #
def initialize_system():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🔹 JARVIS Assistant Booting Up...")
    # Use the new speak function with stop capability
    global ui_instance
    if 'ui_instance' in globals():
        ui_instance.speak_with_stop("Jarvis system initializing, please wait.")
    else:
        speak("Jarvis system initializing, please wait.")
    time.sleep(1)
    print("✅ System initialized successfully.\n")

def start_reminder_loop():
    reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
    reminder_thread.start()

# ====== MAIN LOOP ====== #
async def main_loop():
    while True:
        print("🎤 Waiting for wake word ('Jarvis')...")
        if listen_for_wake_word():
            if 'ui_instance' in globals():
                ui_instance.speak_with_stop("Yes?")
            
               
            
            if not authenticate_user():
                if 'ui_instance' in globals():
                    ui_instance.speak_with_stop("Access denied. Please try again.")
                else:
                    speak("Access denied. Please try again.")
                continue
            
            try:
                result = await fixed_execute_command(ui_instance if 'ui_instance' in globals() else None)
                if result == "exit":
                    if 'ui_instance' in globals():
                        ui_instance.speak_with_stop("Goodbye, shutting down.")
                    else:
                        speak("Goodbye, shutting down.")
                    break
            except Exception as e:
                print(f"❌ Error executing command: {e}")
                if 'ui_instance' in globals():
                    ui_instance.speak_with_stop("Sorry, I encountered an error.")
                else:
                    speak("Sorry, I encountered an error.")
        else:
            await asyncio.sleep(1)

# ====== ENTRY POINT ====== #
if __name__ == "__main__":
    # Create UI instance first
    ui = JarvisUI()
    ui_instance = ui  # Make it globally accessible
    
    initialize_system()
    start_reminder_loop()

    # Start voice loop in separate thread
    voice_thread = threading.Thread(
        target=lambda: asyncio.run(main_loop()), 
        daemon=True
    )
    voice_thread.start()
    
    # Run UI
    ui.run()