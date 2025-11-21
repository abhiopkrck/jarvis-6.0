import os
import re
from gtts import gTTS
import pygame
from langdetect import detect

# 🌍 Supported & fallback language map
LANGUAGE_MAP = {
    "zh-cn": "zh",  # Simplified Chinese
    "zh-tw": "zh",  # Traditional Chinese
    "no": "sv",     # Norwegian → Swedish
    "id": "en",     # Indonesian → English fallback
    "vi": "en",     # Vietnamese → English fallback
    "ko": "ko",     # Korean
    "ja": "ja",     # Japanese
    "fr": "fr",     # French
    "es": "es",     # Spanish
    "de": "de",     # German
    "it": "it",     # Italian
    "pt": "pt",     # Portuguese
    "hi": "hi",     # Hindi
    "en": "en",     # English
}


def clean_text(text: str) -> str:
    """
    Clean unwanted symbols, emojis, or control characters from text.
    Keeps punctuation for natural speech.
    """
    if not text:
        return ""
    # Remove symbols that sound weird when spoken
    text = re.sub(r"['#@^%*_=~<>\,`\/\[\]{}|!@#$%^&*(){}_+|?>,<./]", "", text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def speak(text: str):
    """Speak text aloud with multi-language support and cleaned input."""
    if not text or not text.strip():
        print("[speak()]: Nothing to speak.")
        return

    try:
        # 🧹 Clean text before speaking
        text = clean_text(text)

        # 🔍 Detect language
        lang = detect(text)
        lang = LANGUAGE_MAP.get(lang, "en")
        print(f"[🌐 Detected language]: {lang}")

        # 🗣️ Generate speech
        temp_dir = os.path.join(os.getcwd(), "temp_audio")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, "output.mp3")

        tts = gTTS(text=text, lang=lang)
        tts.save(temp_path)

        # 🎧 Play via pygame
        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        # Wait till finished
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove(temp_path)

    except Exception as e:
        print(f"[❌ Error in speak()]: {e}")
