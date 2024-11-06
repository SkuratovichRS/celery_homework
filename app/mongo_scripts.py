from bson import ObjectId
from flask_pymongo import MongoClient
from gridfs import GridFS, errors


def store_image(image: bytes, client: MongoClient) -> str:
    db = client["upscale"]
    fs = GridFS(db)
    image_id = fs.put(image)
    print(image_id)
    return str(image_id)


def get_image(image_id: str, client: MongoClient) -> bytes:
    db = client["upscale"]
    fs = GridFS(db)
    try:
        image_id = ObjectId(image_id)
        image = fs.get(image_id).read()
        return image
    except errors.NoFile:
        return None
