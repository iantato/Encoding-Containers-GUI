from flask import Flask

from app.home.base import home_bp
from app.encode.base import encoding_bp


def create_app() -> Flask:
    app = Flask(__name__)
    
    register_blueprint(app)

    return app


def register_blueprint(app : Flask):
    
    app.register_blueprint(home_bp)
    app.register_blueprint(encoding_bp)