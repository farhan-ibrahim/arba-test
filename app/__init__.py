from flask import Flask

def create_app():
    from . import models, views, services
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my.db'  # Path to SQLite database
    models.init_app(app)
    views.init_app(app)
    services.init_app(app)
    return app

