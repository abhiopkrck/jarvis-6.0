def parse_command(command_text):
    """Parse the user's voice command and return intent + data."""
    command_text = command_text.lower()
    
    if "open" in command_text:
        return "open_app", command_text.replace("open ", "")
    
    elif "search" in command_text:
        return "search_web", command_text.replace("search ", "")
    
    elif "play music" in command_text:
        return "play_music", ""
    
    elif "play on youtube" in command_text:
        return "play_youtube", ""
    
    elif "reminder" in command_text:
        return "set_reminder", command_text
    
    elif "read text" in command_text:
        return "read_text", command_text
    
    elif any(x in command_text for x in ["screenshot", "capture screen", "save screenshot"]):
        return "take_screenshot", ""
    
    elif any(x in command_text for x in ["record thhis vedio", "capture screen vedio", "screen recording on karo","is game ka vedio banavo","iski recording chalu kardo ","turn on screen recorder"]):
        return "take_screenshot", ""

    else:
        return "unknown", command_text
