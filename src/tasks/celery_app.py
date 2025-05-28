from celery import Celery
from src.config.settings import get_settings

settings = get_settings()

celery = Celery(
    "celery_worker",
    broker=settings.redis_url,  # ✅ TO‘G‘RI
    backend=settings.redis_url,  # ✅ TO‘G‘RI
    include=[
        "src.tasks.email",
        "src.tasks.send_warnings",
    ],  # ✅ import path ham to‘g‘rilandi
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Tashkent",
    enable_utc=True,
)
