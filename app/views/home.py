from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from flask_restful import Resource

from app.models import Posts, db
from app.views.error import handle_error

home = Blueprint('home', __name__)
class Home(Resource):
    # Public Endpoints
    @home.route('/', methods=['GET'])
    def get():
        return jsonify({
            'status': 'success',
            'message': 'Welcome to the home page'
        }), 200