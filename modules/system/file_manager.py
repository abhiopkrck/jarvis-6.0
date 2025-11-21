# modules/system/file_manager.py
import os
import asyncio
import shutil

async def create_file(file_path: str):
    """
    Create a new empty file.
    """
    with open(file_path, "w") as f:
        pass
    print(f"[System] File created: {file_path}")

async def delete_file(file_path: str):
    """
    Delete a file.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"[System] File deleted: {file_path}")
    else:
        print(f"[System] File not found: {file_path}")

async def move_file(src: str, dst: str):
    """
    Move file from source to destination.
    """
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"[System] File moved from {src} to {dst}")
    else:
        print(f"[System] Source file not found: {src}")
