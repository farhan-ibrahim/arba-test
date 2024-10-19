
from flask import Blueprint, jsonify, request
from flask_login import login_required, login_user, logout_user
from flask_restful import Resource
import werkzeug
import werkzeug.security

from app.models import Users
from firestore import db, firestore
from app.views.error import handle_error


auth = Blueprint('auth', __name__)
class Auth(Resource):  
    @auth.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST':
            args = request.get_json()

            # Check if email is already in use
            if db.collection('users').where('email', '==', args['email']).get():
                return jsonify({'status': 'error', 'message': 'Email already exists'}), 400           

            try:
                email = args['email']
                password = args['password']
                name = args['name']
              
                update_time, user_ref = db.collection('users').add({
                    'email': email,
                    'name': name,
                    'password': werkzeug.security.generate_password_hash(password),
                    'created_at': firestore.SERVER_TIMESTAMP,
                    'updated_at': firestore.SERVER_TIMESTAMP,
                })

                user = Users(email=email, name=name)
                user.set_password(password)

                # Fetch the created user using email instead of ID (reduces DB query)
                user = db.collection('users').document(user_ref.id).get()

                return jsonify({
                    'status': 'success',
                    'data': {
                        'id': user.id,
                        'email': user.get("email"),
                        'name': user.get("name")
                    }
                }), 200
            except Exception as e:
                handle_error(e, request)
        
    @auth.route('/login', methods=['GET','POST'])
    def login():
        args = request.get_json()
        email = args['email']
        password = args['password']
        users = db.collection('users').where('email','==', email).get()
        
        if not users or len(users) == 0:
            print('User not found')
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404
        
        user = users[0]
        if not werkzeug.security.check_password_hash(user.get("password"), password):
            print('Invalid credentials')
            return jsonify({ 
                'status': 'error',
                'message': 'Invalid credentials'
            }), 401
        
        try:
            login = login_user(Users(id=user.id))
            if login:
                return jsonify({
                    'status': 'success',
                    'data': {
                        'id': user.id,
                        'email': user.get("email"),
                        'name': user.get("name")
                    }
                }), 200
            else : 
                return jsonify({
                    'status': 'error',
                    'message': 'Login failed'
                }), 401
        except Exception as e:
            handle_error(e, request)
    
    @auth.route('/logout')
    @login_required
    def logout():
        try:
            logout = logout_user()
            if logout:
                return jsonify({
                    'status': 'success',
                    'message': 'Logged out successfully'
                }), 200
        except Exception as e:
            handle_error(e, request)