from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from flask_restful import Resource

from app.models import Comments, db
from app.views.error import handle_error

comment = Blueprint('comment', __name__, url_prefix='/comment')
class Comment(Resource):
    @comment.route('/create', methods=['POST'])
    @login_required
    def create():
        if request.method == 'POST':
            try:
                args = request.get_json()
                text = args['text']
                post_id = args['post_id']
                comment = Comments(text=text, post_id=post_id, user_id=current_user.id)
                db.session.add(comment)
                db.session.commit()
                return jsonify({
                    'status': 'success',
                    'data': {
                        'id': comment.id,
                        'text': comment.text,
                        'post_id': comment.post_id,
                        'user_id': comment.user_id
                    }
                }), 200
            except Exception as e:
                handle_error(e, request)
        else:
            return jsonify({
                'status': 'failed',
                'message': 'Invalid request method'
            }), 405
        
    @comment.route('/delete/<int:comment_id>', methods=['DELETE'])
    @login_required
    def delete(comment_id):
        try:
            comment = Comments.query.filter_by(id=comment_id).first()
            if not comment:
                return jsonify({
                    'status': 'error',
                    'message': 'Comment not found'
                }), 404

            if comment.user_id != current_user.id:
                return jsonify({
                    'status': 'error',
                    'message': 'Unauthorized'
                }), 401
            
            db.session.delete(comment)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'data': None
            }), 200
        except Exception as e:
            handle_error(e, request)


    @comment.route('/update/<int:comment_id>', methods=['PUT'])
    @login_required
    def update(comment_id):
        try:
            comment = Comments.query.filter_by(id=comment_id).first()
            if not comment:
                return jsonify({
                    'status': 'error',
                    'message': 'Post not found'
                }), 404

            if comment.user_id != current_user.id:
                return jsonify({
                    'status': 'error',
                    'message': 'Unauthorized'
                }), 401

            args = request.get_json()
            text = args['text']

            comment.text = text
            db.session.commit()
            return jsonify({
                'status': 'success',
                'data': {
                    'id': comment.id,
                    'text': comment.text,
                    'post_id': comment.post_id,
                    'user_id': comment.user_id
                }
            }), 200
        except Exception as e:
            handle_error(e, request)