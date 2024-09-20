from flask import Flask
from .routes.main import main
from .routes.api import api


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.register_blueprint(main)
    app.register_blueprint(api)

    return app
