from celery.result import AsyncResult
from cv2 import dnn_superres

from app.factory import Factory
from app.upscale.upscale import setup_scaler, upscale

factory = Factory()
celery_app = factory.create_celery_app()


def get_task(task_id: str) -> AsyncResult:
    return AsyncResult(task_id, app=celery_app)


@celery_app.task
def scale_image(
    img_bytes: bytes, scaler: dnn_superres.DnnSuperResImpl = setup_scaler()
) -> bytes:
    return upscale(img_bytes, scaler)
