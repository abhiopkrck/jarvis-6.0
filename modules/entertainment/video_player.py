import re
import pywhatkit as kit

def extract_yt_term(command: str):
    """
    Extracts text between 'play' and 'on youtube' from the voice command.
    Example: 'play despacito on youtube' → 'despacito'
    """
    if not command:
        return None
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None

def play_youtube(command: str):
    """
    Plays the requested YouTube video using pywhatkit.
    """
    search_term = extract_yt_term(command)
    if search_term:
        print(f"[YouTube] Playing: {search_term}")
        kit.playonyt(search_term)
    else:
        print("[YouTube] Could not understand the video name.")
