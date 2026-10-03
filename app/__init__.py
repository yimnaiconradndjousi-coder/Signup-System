from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes.auth import auth
from app.routes.register import register

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, origins=[
    "http://localhost:8080",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
    ], supports_credentials = True)

    app.register_blueprint(auth)
    app.register_blueprint(register)
    return app

	