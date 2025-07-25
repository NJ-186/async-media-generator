import os

from app.config.config import settings


async def save_media(file_bytes: bytes, filename: str) -> str:
    path = os.path.join(settings.STORAGE_PATH, filename)
    os.makedirs(settings.STORAGE_PATH, exist_ok=True)
    with open(path, "wb") as f:
        f.write(file_bytes)
    return path
