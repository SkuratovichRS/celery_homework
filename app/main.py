from app.factory import Factory
from app.urls import blueprint


def main():
    factory = Factory()
    flask_app = factory.create_flask_app()
    flask_app.register_blueprint(blueprint)
    flask_app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()