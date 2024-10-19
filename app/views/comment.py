from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from flask_restful import Resource

from firestore import db, firestore
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
                print(current_user.id)
                update_time, comment_ref = db.collection('comments').add({
                    'text': text,
                    'post_id': post_id,
                    'user_id': current_user.id,
                    'created_at': firestore.SERVER_TIMESTAMP,
                    'updated_at': firestore.SERVER_TIMESTAMP
                })

                comment = db.collection('comments').document(comment_ref.id).get()
        
                return jsonify({
                    'status': 'success',
                    'data': {
                        'id': comment_ref.id,
                        'text': comment.get("text"),
                        'post_id': comment.get("post_id"),
                        'user_id': comment.get("user_id")
                    }
                }), 200
            except Exception as e:
                handle_error(e, request)
        else:
            return jsonify({
                'status': 'failed',
                'message': 'Invalid request method'
            }), 405
        
    @comment.route('/delete/<string:comment_id>', methods=['DELETE'])
    @login_required
    def delete(comment_id):
        try:
            comment = db.collection('comments').document(comment_id).get()
            if not comment:
                return jsonify({
                    'status': 'error',
                    'message': 'Comment not found'
                }), 404

            if comment.get("user_id") != current_user.id:
                return jsonify({
                    'status': 'error',
                    'message': 'Unauthorized'
                }), 401
            
            db.collection('comments').document(comment_id).delete()
            return jsonify({
                'status': 'success',
                'data': None
            }), 200
        except Exception as e:
            handle_error(e, request)


    @comment.route('/update/<string:comment_id>', methods=['PUT'])
    @login_required
    def update(comment_id):
        try:
            comment = db.collection('comments').document(comment_id).get()
            if not comment:
                return jsonify({
                    'status': 'error',
                    'message': 'Post not found'
                }), 404

            if comment.get("user_id") != current_user.id:
                return jsonify({
                    'status': 'error',
                    'message': 'Unauthorized'
                }), 401

            args = request.get_json()
            text = args['text']

            db.collection('comments').document(comment_id).update({
                'text': text,
                'updated_at': firestore.SERVER_TIMESTAMP
            })

            updated_comment = db.collection('comments').document(comment_id).get()

            return jsonify({
                'status': 'success',
                'data': {
                    'id': updated_comment.id,
                    'text': updated_comment.get("text"),
                    'post_id': updated_comment.get("post_id"),
                    'user_id': updated_comment.get("user_id")
                }
            }), 200
        except Exception as e:
            handle_error(e, request)