# modules/system/screenshot.py
import pyautogui
import datetime
import asyncio
import os

async def take_screenshot():
    """
    Take a screenshot and save it to screenshots folder.
    """
    os.makedirs("screenshots", exist_ok=True)
    filename = f"screenshots/screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"[System] Screenshot saved: {filename}")
