from celery.result import AsyncResult
from cv2 import dnn_superres

from app.factory import Factory
from app.mongo_scripts import store_image
from app.upscale.upscale import upscale

factory = Factory()
celery_app = factory.create_celery_app()
mongo_client = factory.create_mongo_client()
scaler = factory.create_scaler()


def get_task(task_id: str) -> AsyncResult:
    return AsyncResult(task_id, app=celery_app)


@celery_app.task
def scale_image(img_bytes: bytes) -> bytes:
    img_bytes = upscale(img_bytes, scaler)
    image_id = store_image(img_bytes, mongo_client)
    return image_id
