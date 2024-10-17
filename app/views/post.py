from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from flask_restful import Resource

from app.models import Posts, db
from app.views.error import handle_error

post = Blueprint('post', __name__, url_prefix='/post')
class Post(Resource):
    @post.route('/all', methods=['GET'])
    @login_required
    def all():
        try:
            posts = Posts.query.filter_by(user_id=current_user.id).all()
            data = []
            for post in posts:
                data.append({
                    'id': post.id,
                    'image': post.image_url,
                    'caption': post.caption,
                    'user_id': post.user_id
                })
            return jsonify({
                'status': 'success',
                'data': data
            }), 200
        except Exception as e:
            handle_error(e, request)

    @post.route('/create', methods=['GET','POST'])
    @login_required
    def create():
        if request.method == 'POST':
            try:
                image = request.form['image']
                caption = request.form['caption']
                post = Posts(image_url=image, caption=caption, user_id=current_user.id)
                db.session.add(post)
                db.session.commit()
                return jsonify({
                    'status': 'success',
                    'data': {
                        'id': post.id,
                        'image': post.image_url,
                        'caption': post.caption,
                        'user_id': post.user_id
                    }
                }), 200
            except Exception as e:
                handle_error(e, request)
        else:
            return jsonify({
                'status': 'failed',
                'message': 'Invalid request method'
            }), 405
        
    @post.route('/delete/<int:post_id>', methods=['DELETE'])
    @login_required
    def delete(post_id):
        try:
            post = Posts.query.filter_by(id=post_id).first()
            if not post:
                return jsonify({
                    'status': 'error',
                    'message': 'Post not found'
                }), 404

            if post.user_id != current_user.id:
                return jsonify({
                    'status': 'error',
                    'message': 'Unauthorized'
                }), 401
            
            db.session.delete(post)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'data': None
            }), 200
        except Exception as e:
            handle_error(e, request)


    @post.route('/update/<int:post_id>', methods=['PUT'])
    @login_required
    def update(post_id):
        try:
            post = Posts.query.filter_by(id=post_id).first()
            if not post:
                return jsonify({
                    'status': 'error',
                    'message': 'Post not found'
                }), 404

            if post.user_id != current_user.id:
                return jsonify({
                    'status': 'error',
                    'message': 'Unauthorized'
                }), 401

            image = request.form['image']
            caption = request.form['caption']
            post.image_url = image
            post.caption = caption
            db.session.commit()
            return jsonify({
                'status': 'success',
                'data': {
                    'id': post.id,
                    'image': post.image_url,
                    'caption': post.caption,
                    'user_id': post.user_id
                }
            }), 200
        except Exception as e:
            handle_error(e, request)