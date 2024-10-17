from .auth import auth
from .post import post
from .comment import comment

def init_app(app):
    app.register_blueprint(auth)
    app.register_blueprint(post)
    app.register_blueprint(comment)
    return app