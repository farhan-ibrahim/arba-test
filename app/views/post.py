from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from flask_restful import Resource

from firestore import db, firestore
from app.views.error import handle_error

post = Blueprint('post', __name__)
class Post(Resource):
    # Public Endpoints
    @post.route('/posts/all', methods=['GET'])
    def get_all_posts():
        try:
            limit = request.args.get('limit', 10)
            posts = db.collection('posts').limit(limit).get()
            data = []
            for post in posts:
                user = db.collection('users').document(str(post.get("user_id"))).get()
                comments = []
                post_comments = db.collection('comments').where('post_id', '==', post.id).get()
                for comment in post_comments:
                    comments.append({
                        'id': comment.id,
                        'text': comment.get("text"),
                        'user_id': comment.get("user_id"),
                        # 'author': author.get("name")
                    })

                data.append({
                    'id': post.id,
                    'image': post.get("image_url"),
                    'caption': post.get("caption"),
                    'user_id': post.get("user_id"),
                    'author': user.get("name"),
                    'comments': comments,
                    'comments_count': len(post_comments)
                })
            return jsonify({
                'status': 'success',
                'data': data
            }), 200
        except Exception as e:
            handle_error(e, request)

    @post.route('/post/<string:post_id>', methods=['GET'])
    def get_by_id(post_id):
        try:
            post = db.collection('posts').document(post_id).get()

            if not post:
                return jsonify({
                    'status': 'error',
                    'message': 'Post not found'
                }), 404
            
            comments = []
            post_comments = db.collection('comments').where('post_id', '==', post.id).get()
            for comment in post_comments:
                comments.append({
                    'id': comment.id,
                    'text': comment.get("text"),
                    'user_id': comment.get("user_id"),
                })
            
            return jsonify({
                'status': 'success',
                'data': {
                    'id': post.id,
                    'image': post.get("image_url"),
                    'caption': post.get("caption"),
                    'user_id': post.get("user_id"),
                    'comments': comments,
                }
            }), 200
        except Exception as e:
            handle_error(e, request)

    @post.route('/posts', methods=['GET'])
    @login_required
    def get_all_user_posts():
        try:
            limit = request.args.get('limit', 10)
            posts = db.collection('posts').where('user_id', '==', current_user.id).limit(limit).get()
            # posts = Posts.query.filter_by(user_id=current_user.id).limit(limit).all()
            data = []
            for post in posts:
                comments = []
                post_comments = db.collection('comments').where('post_id', '==', int(post.id)).get()
                for comment in post_comments:
                    comments.append({
                        'id': comment.id,
                        'text': comment.get("text"),
                        'user_id': comment.get("user_id")
                    })

                data.append({
                    'id': post.id,
                    'image': post.get("image_url"),
                    'caption': post.get("caption"),
                    'user_id': post.get("user_id"),
                    'comments': comments,
                    'comments_count': len(post_comments)
                })
            return jsonify({
                'status': 'success',
                'data': data
            }), 200
        except Exception as e:
            handle_error(e, request)

    @post.route('/post/<string:post_id>/comments', methods=['GET'])
    def get_post_comments(post_id):
        try:
            post = db.collection('posts').document(str(post_id)).get()
            # post = Posts.query.filter_by(id=post_id).first()

            if not post:
                return jsonify({
                    'status': 'error',
                    'message': 'Post not found'
                }), 404
            
            data = []
            post_comments = db.collection('comments').where('post_id', '==', int(post.id)).get()
            for comment in post_comments:
                data.append({
                    'id': comment.id,
                    'text': comment.get("text"),
                    'user_id': comment.get("user_id")
                })
            
            return jsonify({
                'status': 'success',
                'data': data
            }), 200
        except Exception as e:
            handle_error(e, request)

    @post.route('/post/create', methods=['GET','POST'])
    @login_required
    def create():
        if request.method == 'POST':
            try:
                args = request.get_json()
                image = args['image']
                caption = args['caption']

                update_time, post_ref = db.collection('posts').add({
                    'image_url': image,
                    'caption': caption,
                    'user_id': current_user.id,
                    'created_at': firestore.SERVER_TIMESTAMP,
                    'updated_at': firestore.SERVER_TIMESTAMP
                })
                post = db.collection('posts').document(post_ref.id).get()
                return jsonify({
                    'status': 'success',
                    'data': {
                        'id': post_ref.id,
                        'image': post.get("image_url"),
                        'caption': post.get("caption"),
                        'user_id': post.get("user_id")
                    }
                }), 200
            except Exception as e:
                handle_error(e, request)
        else:
            return jsonify({
                'status': 'failed',
                'message': 'Invalid request method'
            }), 405
        
    @post.route('/post/delete/<string:post_id>', methods=['DELETE'])
    @login_required
    def delete(post_id):
        try:
            post = db.collection('posts').document(post_id).get()
            if not post:
                return jsonify({
                    'status': 'error',
                    'message': 'Post not found'
                }), 404

            if post.get("user_id") != current_user.id:
                return jsonify({
                    'status': 'error',
                    'message': 'Unauthorized'
                }), 401
            
            db.collection('posts').document(post_id).delete()
            
            return jsonify({
                'status': 'success',
                'data': None
            }), 200
        except Exception as e:
            handle_error(e, request)


    @post.route('/post/update/<string:post_id>', methods=['PUT'])
    @login_required
    def update(post_id):
        try:
            post = db.collection('posts').document(post_id).get()
            if not post:
                return jsonify({
                    'status': 'error',
                    'message': 'Post not found'
                }), 404

            if post.get("user_id") != current_user.id:
                return jsonify({
                    'status': 'error',
                    'message': 'Unauthorized'
                }), 401

            args = request.get_json()
            image = args['image']
            caption = args['caption']
        
            db.collection('posts').document(post_id).update({
                'image_url': image,
                'caption': caption,
                'updated_at': firestore.SERVER_TIMESTAMP
            })

            updated_post = db.collection('posts').document(post_id).get()

            return jsonify({
                'status': 'success',
                'data': {
                    'id': updated_post.id,
                    'image': updated_post.get("image_url"),
                    'caption': updated_post.get("caption"),
                    'user_id': updated_post.get("user_id")
                }
            }), 200
        except Exception as e:
            handle_error(e, request)