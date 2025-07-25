import httpx

from app.config.config import settings


async def generate_image(prompt: str, parameters: str) -> bytes:
    # Mocking Image generation
    async with httpx.AsyncClient() as client:
        ### Option 1 : SUCCESS ###
        return b"image-bytes"
        ### Option 2 : FAILURE WITHOUT EXCEPTION ###
        # return None
        ### Option 3 : FAILURE WITH EXCEPTION  ###
        # raise Exception("Issue generating image.")
