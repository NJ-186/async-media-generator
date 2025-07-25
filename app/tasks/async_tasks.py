import asyncio

from app.config.celery_app import celery
from app.crud.job import get_job, update_job
from app.services.job_processor import process_job


@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_backoff_max=60, retry_jitter=True, max_retries=5)
def generate_media(self, job_id: str):
    def run_async(coro):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    try:
        job = run_async(get_job(job_id))
        # Uncomment the following line if you want to test retries.
        # raise Exception("Exception in code !!")

        if job:
            run_async(process_job(job_id, job.prompt, job.parameters))
    except Exception as exc:
        try:
            run_async(update_job(job_id))
        except Exception as db_exc:
            print(f"Failed to update retry count in DB: {db_exc}")
            raise self.retry(exc=exc)
