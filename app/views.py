from flask import jsonify, request
from flask.views import MethodView

from app.celery_scripts import get_task, scale_image
from app.factory import Factory
from app.mongo_scripts import get_image

factory = Factory()
mongo_client = factory.create_mongo_client()


class Upscale(MethodView):
    def post(self) -> tuple[jsonify, int]:
        request_files = request.files
        if not request_files or not request_files.get("file"):
            return jsonify({"error": "No file in request"}), 400
        if len(request_files) != 1:
            return jsonify({"error": "Too many files in request"}), 400
        img_bytes: bytes = request_files.get("file").read()
        task = scale_image.delay(img_bytes)
        return jsonify({"task_id": task.id}), 200

    def get(self, task_id: str) -> tuple[jsonify, int]:
        task = get_task(task_id)
        if task.result is not None:
            return jsonify({"status": task.status, "result": task.result}), 200
        return jsonify({"status": task.status, "result": "Not ready"}), 200


class Image(MethodView):
    def get(self, image_id: str) -> tuple[jsonify, int]:
        image = get_image(image_id, mongo_client)
        if not image:
            return jsonify({"error": "Image not found"}), 404
        return image, 200
