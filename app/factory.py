import pymongo
from celery import Celery
from flask import Flask

from app.settings import Settings
from app.upscale.upscale import setup_scaler


class Factory:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Factory, cls).__new__(cls)
            cls._instance._settings = Settings
            cls._instance._singleton = {}
        return cls._instance

    def create_flask_app(self) -> Flask:
        if not self._singleton.get("flask_app"):
            self._singleton["flask_app"] = Flask(__name__)
        return self._singleton["flask_app"]

    def create_celery_app(self):
        if not self._singleton.get("celery_app"):
            celery_obj = Celery(
                __name__, broker=self._settings.CELERY_BROKER_URL, backend=self._settings.CELERY_BACKEND_URL
            )
            flask_app = self.create_flask_app()
            celery_obj.conf.update(flask_app.config)

            class ContextTask(celery_obj.Task):
                def __call__(self, *args, **kwargs):
                    with flask_app.app_context():
                        return self.run(*args, **kwargs)

            celery_obj.Task = ContextTask
            self._singleton["celery_app"] = celery_obj
        return self._singleton["celery_app"]

    def create_mongo_client(self):
        if not self._singleton.get("mongo_client"):
            self._singleton["mongo_client"] = pymongo.MongoClient(self._settings.MONGO_URI)
        return self._singleton["mongo_client"]

    def create_scaler(self):
        if not self._singleton.get("scaler"):
            self._singleton["scaler"] = setup_scaler()
        return self._singleton["scaler"]