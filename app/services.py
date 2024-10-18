
from flask import jsonify
from flask_login import LoginManager
from app.models import Users

login_manager = LoginManager()
login_manager.login_view = 'login'  # Specify the login route

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@login_manager.request_loader
def request_loader(request):
    email = request.headers.get('Authorization')
    user = Users.query.filter_by(email=email).first()
    return user if user else None

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({
        'status': 'error',
        'message': 'Unauthorized'
    }), 401

def init_app(app):
    login_manager.init_app(app)