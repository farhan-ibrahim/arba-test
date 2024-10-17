from .auth import auth
from .post import post

def init_app(app):
    app.register_blueprint(auth)
    app.register_blueprint(post)
    return app