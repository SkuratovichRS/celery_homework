from types import SimpleNamespace

import pytest
from gridfs import GridFS

from app.urls import blueprint
from app.views import factory, mongo_client

flask_app = factory.create_flask_app()
flask_app.register_blueprint(blueprint)


def test_image_view():
    with open("tests/data/small_lama.png", "rb") as image_file:
        image_bytes = image_file.read()
    db = mongo_client["upscale"]
    fs = GridFS(db)
    image_id = fs.put(image_bytes)
    image_id = str(image_id)
    with flask_app.test_client() as client:
        url = f"processed/{image_id}"
        response = client.get(url)
        print(response.data)
        assert response.status_code == 200
        assert response.data == image_bytes


def test_image_view_bad_request():
    with flask_app.test_client() as client:
        url = f"processed/672d04b059f48ba1ba9cb37b"
        response = client.get(url)
        assert response.status_code == 404
        assert response.json == {"error": "Image not found"}


def test_post_upscale_view(mocker):
    mocker.patch("app.views.scale_image.delay", return_value=SimpleNamespace(id="task_id"))
    with flask_app.test_client() as client:
        url = "upscale"
        with open("tests/data/small_lama.png", "rb") as image_file:
            data = {"file": (image_file, "small_lama.png")}
            response = client.post(url, data=data, content_type="multipart/form-data")
            assert response.status_code == 200
            assert response.json == {"task_id": "task_id"}


def test_post_upscale_view_no_file():
    with flask_app.test_client() as client:
        url = "upscale"
        response = client.post(url)
        assert response.status_code == 400
        assert response.json == {"error": "No file in request"}


def test_post_upscale_more_then_one_file():
    with flask_app.test_client() as client:
        url = "upscale"
        with open("tests/data/small_lama.png", "rb") as image_file:
            with open("tests/data/small_lama.png", "rb") as image_file_2:
                data = {"file": (image_file, "small_lama.png"), "file_2": (image_file_2, "small_lama.png")}
                response = client.post(url, data=data, content_type="multipart/form-data")
                assert response.status_code == 400
                assert response.json == {"error": "Too many files in request"}


@pytest.mark.parametrize(
    "simplenamespace, json_response",
    [
        (SimpleNamespace(status="SUCCESS", result="result"), {"status": "SUCCESS", "result": "result"}),
        (SimpleNamespace(status="PENDING", result=None), {"status": "PENDING", "result": "Not ready"}),
    ],
)
def test_get_upscale_view(mocker, simplenamespace, json_response):
    mocker.patch("app.views.get_task", return_value=simplenamespace)
    with flask_app.test_client() as client:
        url = "tasks/task_id"
        response = client.get(url)
        assert response.status_code == 200
        assert response.json == json_response
