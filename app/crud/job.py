from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.session import engine
from app.models.job import Job


async def create_job(job_id: str, job_data):
    async with AsyncSession(engine) as session:
        async with session.begin():
            job = Job(id=job_id, prompt=job_data.prompt, parameters=job_data.parameters)
            session.add(job)


async def get_job(job_id: str):
    async with AsyncSession(engine) as session:
        result = await session.exec(select(Job).where(Job.id == job_id))
        return result.first()


async def update_job(
    job_id: str,
    increment_retry: bool = False,
    status: Optional[str] = None,
    result_url: Optional[str] = None,
    error: Optional[str] = None,
):
    async with AsyncSession(engine) as session:
        result = await session.exec(select(Job).where(Job.id == job_id))
        job = result.first()
        if not job:
            return None

        if increment_retry:
            job.retry_count = (job.retry_count or 0) + 1

        if status is not None:
            job.status = status
        if result_url is not None:
            job.result_url = result_url
        if error is not None:
            job.error = error

        session.add(job)
        await session.commit()
        return job
