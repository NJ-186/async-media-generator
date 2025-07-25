from celery import Celery

from app.config.config import settings

celery = Celery(
    "worker",
    broker=settings.BROKER_URL,
    backend=settings.RESULT_BACKEND,
)
celery.conf.update(
    task_serializer="json", result_serializer="json", accept_content=["json"], timezone="UTC", enable_utc=True, imports=["app.tasks.async_tasks"]
)
