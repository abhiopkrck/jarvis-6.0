# modules/voice/wake_word.py
import speech_recognition as sr
import eel

WAKE_WORDS = ["abhishek","jarvis","suno jarvis","ok jarvis","ok nobita","naruto","itachi"]

def listen_for_wake_word():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for wake word...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio).lower()
        for word in WAKE_WORDS:
            if word in text:
                return True
        return False
    except sr.UnknownValueError:
        return False
    except sr.RequestError:
        print("Speech recognition service error")
        return False
