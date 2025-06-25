
from flask import Flask
from flasgger import Swagger
from app.routes.creators import creators_bp

def create_app():
    app = Flask(__name__)
    Swagger(app)
    app.register_blueprint(creators_bp)
    return app
