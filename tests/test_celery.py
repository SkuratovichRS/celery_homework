import pytest
from bson import ObjectId
from gridfs import GridFS

from app.celery_scripts import mongo_client, scale_image


def test_scale_image():
    with open("tests/data/small_lama.png", "rb") as image_file:
        image_bytes = image_file.read()
    img_id = scale_image(image_bytes)
    img_id = ObjectId(img_id)
    db = mongo_client["upscale"]
    fs = GridFS(db)
    image = fs.get(img_id).read()
    assert image is not None

def test_scale_image_bad_image():
    with pytest.raises(Exception):
        scale_image(b"bad image")