import cv2
import numpy as np
from cv2 import dnn_superres

from app.settings import Settings


def setup_scaler(model_path: str = Settings.MODEL_PATH) -> dnn_superres.DnnSuperResImpl:
    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel("edsr", 2)
    return scaler


def upscale(image_bytes: bytes, scaler: dnn_superres.DnnSuperResImpl) -> bytes:
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    result = scaler.upsample(image)
    ndarray = cv2.imencode(".png", result)[1]
    return ndarray.tobytes()


def example():
    image = cv2.imread("lama_300px.png")
    success, encoded_image = cv2.imencode('.png', image)
    if success:
        bts = encoded_image.tobytes() 
    else:
        raise ValueError("Failed to encode image")
    
    return upscale(bts, setup_scaler())


if __name__ == "__main__":
    print(example())
