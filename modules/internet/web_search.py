# modules/internet/web_search.py
import webbrowser
import asyncio

async def search_web(query: str):
    """
    Open a web browser with a search query.
    """
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    print(f"[Internet] Searching for '{query}'")
