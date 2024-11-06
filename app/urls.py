from flask import Blueprint

from app.views import Image, Upscale

blueprint = Blueprint("api/v1", __name__)

blueprint.add_url_rule("/upscale", view_func=Upscale.as_view("upscale"), methods=["POST"])
blueprint.add_url_rule("/tasks/<string:task_id>", view_func=Upscale.as_view("upscale_task"), methods=["GET"])
blueprint.add_url_rule("/processed/<string:image_id>", view_func=Image.as_view("image"), methods=["GET"])
