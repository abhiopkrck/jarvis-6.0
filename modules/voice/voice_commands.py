import asyncio
from datetime import datetime, timedelta
import speech_recognition as sr

# Relative imports
from .nlu import parse_command
from .tts import speak
from .reminders import add_reminder
from .chat_storage import log_chat

# Absolute imports
from modules.system.app_launcher import launch_app
from modules.internet.web_search import search_web
from modules.entertainment.music_player import play_music
from modules.entertainment.video_player import play_youtube
from modules.entertainment.music_control import handle_music_command
from modules.system.screenshot import take_screenshot
from modules.dev_tools.vscode import ask_jarvis,ask_with_history,HuggingChatbot
from modules.productivity.email_manager import send_email_gmail
from modules.system.notepad_logger import NoteLogger  # ✅ NEW

# Initialize components
logger = NoteLogger()  # ✅ Notepad logger
bot = HuggingChatbot()  # ✅ Single instance for chatbot
username = "Abhishek"

async def execute_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("\n🎤 Listening for your command...\n")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("[Jarvis] Listening...")
        audio = recognizer.listen(source)

    try:
        command_text = recognizer.recognize_google(audio)
        print(f"🧠 You said: {command_text}")

        action, param = parse_command(command_text)
        command = command_text.lower()

        # ---------------- COMMANDS ----------------

        if action == "open_app":
            reply = f"Opening {param}"
            speak(reply)
            await launch_app(param)
            logger.log(command_text, reply)
            log_chat(username, command_text, reply)

        elif "send email" in command:
            speak("Which person?")
            with mic as source:
                audio = recognizer.listen(source)
            name = recognizer.recognize_google(audio).lower().strip()

            speak("What is the subject of your email?")
            with mic as source:
                audio = recognizer.listen(source)
            subject = recognizer.recognize_google(audio).strip()

            speak("What message would you like to send?")
            with mic as source:
                audio = recognizer.listen(source)
            body = recognizer.recognize_google(audio).strip()

            send_email_gmail(name, subject, body)
            reply = f"✅ Email sent to {name}"
            speak(reply)
            logger.log(command_text, reply)
            log_chat(username, command_text, reply)

        elif action == "search_web":
            reply = f"Searching for {param}"
            speak(reply)
            await search_web(param)
            logger.log(command_text, reply)
            log_chat(username, command_text, reply)

        elif "play music" in command:
            reply = "Playing music"
            speak(reply)
            await handle_music_command(command)
            logger.log(command_text, reply)
            log_chat(username, command_text, reply)

        elif "play" in command and "on youtube" in command:
            reply = "Playing on YouTube"
            speak(reply)
            play_youtube(command)
            logger.log(command_text, reply)
            log_chat(username, command_text, reply)

        elif action == "set_reminder":
            reminder_text = param
            reminder_time = datetime.now() + timedelta(seconds=60)
            add_reminder(username, reminder_text, reminder_time)
            reply = f"Reminder set: {reminder_text}"
            speak(reply)
            logger.log(command_text, reply)
            log_chat(username, command_text, reply)

        elif action == "take_screenshot":
            reply = "Taking screenshot"
            speak(reply)
            await take_screenshot()
            logger.log(command_text, reply)
            log_chat(username, command_text, reply)
       
        else:
            response = bot.get_response(command_text, auto_open_notepad=True)
             # ✅ Speak the response
            logger.log(command_text, response)
            log_chat(username, command_text, response)

        return command_text

    except sr.UnknownValueError:
        speak("I could not understand you.")
        return None
    except Exception as e:
        speak("Something went wrong.")
        print("Error:", e)
        return None