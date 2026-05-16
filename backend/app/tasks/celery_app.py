from celery import Celery
from app.config import settings

celery_app = Celery(
    "cognitive_learning_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_always_eager=True,  # Run tasks synchronously for local testing
)

# Optional: define beat schedules here for periodic tasks
celery_app.conf.beat_schedule = {
    # Example: 'train-models-every-night': { ... }
}
