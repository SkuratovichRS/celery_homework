from flask import jsonify, request
from flask.views import MethodView

from app.celery_scripts import get_task, scale_image
from app.exceptions import HttpException
from app.factory import Factory
from app.mongo_scripts import get_image, store_image

factory = Factory()
mongo_client = factory.create_mongo_client()


class Upscale(MethodView):
    def post(self) -> tuple[jsonify, int]:
        request_files = request.files
        if not request_files or not request_files.get("file"):
            raise HttpException(400, "No file in request")
        if len(request_files) != 1:
            raise HttpException(400, "Too many files in request")
        img_bytes: bytes = request_files.get("file").read()
        task = scale_image.delay(img_bytes)
        return jsonify({"task_id": task.id}), 200

    def get(self, task_id: str) -> tuple[jsonify, int]:
        task = get_task(task_id)
        if task.result is not None:
            print(task.result)
            img_id = store_image(task.result, mongo_client)
            return jsonify({"status": task.status, "result": img_id}), 200
        return jsonify({"status": task.status, "result": "Not ready"}), 200


class Image(MethodView):
    def get(self, image_id: str) -> tuple[jsonify, int]:
        image = get_image(image_id, mongo_client)
        if not image:
            raise HttpException(404, "Image not found")
        return image, 200