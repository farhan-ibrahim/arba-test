from flask import Flask
from flask_cors import CORS

import firestore

def create_app():
    from . import models, views, services
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my.db'  # Path to SQLite database
    CORS(app, supports_credentials=True)
    models.init_app(app)
    views.init_app(app)
    services.init_app(app)
    return app

