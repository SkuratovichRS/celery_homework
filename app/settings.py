import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGO_INITDB_DATABASE = os.getenv("MONGO_INITDB_DATABASE")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL")
    MONGO_URI = os.getenv("MONGO_URI")
    MODEL_PATH = os.getenv("MODEL_PATH")
