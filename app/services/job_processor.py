from app.crud.job import update_job
from app.services.client import generate_image
from app.services.file import save_media


async def process_job(job_id: str, prompt: str, parameters: str):
    try:
        # Set status to running at the start
        await update_job(job_id, status="running")
        image_bytes = await generate_image(prompt, parameters)
        if image_bytes:
            path = await save_media(image_bytes, f"{job_id}.png")
            await update_job(job_id, status="completed", result_url=path)
        else:
            # If image generation failed but no exception, mark as failed
            await update_job(job_id, status="failed", error="Could not generate image.")
    except Exception as e:
        await update_job(job_id, status="failed", error=str(e))
