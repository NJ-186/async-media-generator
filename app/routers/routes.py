import uuid

from fastapi import APIRouter, HTTPException

from app.crud.job import create_job, get_job
from app.schemas.job import JobCreateRequest, JobStatusResponse
from app.tasks.async_tasks import generate_media

router = APIRouter()


@router.post("/generate", response_model=JobStatusResponse, response_model_exclude_none=True)
async def generate(job: JobCreateRequest):
    job_id = str(uuid.uuid4())
    await create_job(job_id, job)
    generate_media.delay(job_id)
    return JobStatusResponse(id=job_id, status="queued")


@router.get("/status/{job_id}", response_model=JobStatusResponse, response_model_exclude_none=True)
async def status(job_id: str):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse.from_orm(job)
