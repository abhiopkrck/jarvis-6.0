# modules/entertainment/music_player.py
import asyncio
import pyautogui
import time
import webbrowser
import os

async def play_music(song_name=None, platform=None):
    if not song_name:
        song_name = input("Enter song name: ")

    if not platform:
        platform = input("Which platform? (spotify / youtube / system): ").lower()

    print(f"[Entertainment] Playing '{song_name}' on {platform.title()}...")
    await asyncio.sleep(1)

    # ----------- SPOTIFY -------------
    if platform == "spotify":
        print("[Jarvis] Opening Spotify...")
        pyautogui.hotkey("win", "s")
        time.sleep(1)
        pyautogui.write("spotify", interval=0.05)
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(15)  # wait for Spotify to fully load

        print("[Jarvis] Searching for song...")
        pyautogui.hotkey("ctrl", "l")  # focus search bar
        time.sleep(1)
        pyautogui.write(song_name, interval=0.05)
        pyautogui.press("enter")
        time.sleep(5)

        print("[Jarvis] Selecting the second result...")
        for _ in range(3):  # adjust tabs if needed to reach the second song
            pyautogui.press("tab")
            time.sleep(0.2)
        pyautogui.press("enter")
        print("[Jarvis] Second song should now be playing 🎵")


    # ----------- SYSTEM (LOCAL FILE) -------------
    elif platform == "system":
        print("[Jarvis] Trying to play from local system...")
        try:
            os.startfile(f"{song_name}.mp3")
        except Exception as e:
            print(f"[Error] Could not play local file: {e}")

    else:
        print("[Jarvis] Unknown platform. Please say Spotify, YouTube, or System.")

    print("[Jarvis] Enjoy your music 🎧")
