
from flask import Blueprint, jsonify, request
from flask_login import login_required, login_user, logout_user
from flask_restful import Resource

from app.models import Users, db
from app.views.error import handle_error


auth = Blueprint('auth', __name__)
class Auth(Resource):  
    @auth.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST':
            # Check if email is already in use
            if Users.query.filter_by(email=request.form['email']).first():
                return jsonify({'status': 'error', 'message': 'Email already exists'}), 400

            try:
                email = request.form['email']
                password = request.form['password']
                name = request.form['name']
                user = Users(email=email, name=name)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                
                # Fetch the created user using email instead of ID (reduces DB query)
                data = Users.query.filter_by(email=email).first()
                print(user)
                return jsonify({
                    'status': 'success',
                    'data': {
                        'id': data.id,
                        'email': data.email,
                        'name': data.name
                    }
                }), 200
            except Exception as e:
                handle_error(e, request)
        
    @auth.route('/login', methods=['GET','POST'])
    def login():
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()

        if not user:
            print('User not found')
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404
        
        if not user.check_password(password):
            print('Invalid credentials')
            return jsonify({ 
                'status': 'error',
                'message': 'Invalid credentials'
            }), 401
        
        try:
            login = login_user(user)
            if login:
                return jsonify({
                    'status': 'success',
                    'data': {
                        'id': user.id,
                        'email': user.email,
                        'name': user.name
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