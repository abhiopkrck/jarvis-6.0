# modules/features/music_control.py
import asyncio
import re
from modules.entertainment.music_player import play_music

async def handle_music_command(command: str):
    """
    Parse the command text for song name and platform, then call play_music(song, platform).
    Examples it can accept:
      - "play believer on youtube"
      - "play calm playlist on spotify"
      - "play kesariya"  (it will ask platform)
    """
    if not command:
        command = input("Enter play command: ").strip()

    orig = command.strip()
    cmd = orig.lower()

    # default extraction
    song_name = None
    platform = None

    # Detect platform keywords
    if " on spotify" in cmd or " spotify" in cmd:
        platform = "spotify"
    if " on youtube" in cmd or " youtube" in cmd:
        platform = "youtube"
    if " on system" in cmd or " local" in cmd or " system" in cmd:
        platform = "system"

    # Try to extract song name after 'play'
    # This covers: "play <song> on <platform>" and "play <song>"
    m = re.search(r"play\s+(.*)", cmd)
    if m:
        after_play = m.group(1).strip()
        # remove 'on spotify/youtube/system' suffix if present
        after_play = re.sub(r"\s+on\s+(spotify|youtube|system|local)$", "", after_play).strip()
        # set as song_name if non-empty
        if after_play:
            song_name = after_play

    # If not found, try fallback keywords
    if not song_name:
        # remove the word 'music' if user said 'play music'
        cmd2 = cmd.replace("play", "").replace("music", "").strip()
        if cmd2:
            song_name = cmd2

    # Final fallback: prompt user
    if not song_name:
        song_name = input("Which song do you want to play? ").strip()

    print(f"[music_control] Parsed -> song: {song_name!r}, platform: {platform!r}")

    # call music_player with both song and platform (platform can be None -> player will ask)
    try:
        await play_music(song_name, platform)
    except Exception as e:
        print(f"[music_control] Error calling play_music: {e}")
