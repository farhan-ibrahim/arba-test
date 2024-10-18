from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from flask_restful import Resource

from app.models import Posts, db
from app.views.error import handle_error

post = Blueprint('post', __name__)
class Post(Resource):
    # Public Endpoints
    @post.route('/posts/all', methods=['GET'])
    def get_all_posts():
        try:
            limit = request.args.get('limit', 10)
            posts = Posts.query.order_by(Posts.created_at).limit(limit).all()
            data = []
            for post in posts:
                comments = []
                for comment in post.comments:
                    comments.append({
                        'id': comment.id,
                        'text': comment.text,
                        'user_id': comment.user_id,
                        'author': comment.author.name
                    })

                data.append({
                    'id': post.id,
                    'image': post.image_url,
                    'caption': post.caption,
                    'user_id': post.user_id,
                    'author': post.author.name,
                    'comments': comments,
                    'comments_count': len(post.comments)
                })
            return jsonify({
                'status': 'success',
                'data': data
            }), 200
        except Exception as e:
            handle_error(e, request)

    @post.route('/post/<int:post_id>', methods=['GET'])
    def get_by_id(post_id):
        try:
            post = Posts.query.filter_by(id=post_id).first()

            if not post:
                return jsonify({
                    'status': 'error',
                    'message': 'Post not found'
                }), 404
            
            return jsonify({
                'status': 'success',
                'data': {
                    'id': post.id,
                    'image': post.image_url,
                    'caption': post.caption,
                    'user_id': post.user_id,
                    'comments': post.comments
                }
            }), 200
        except Exception as e:
            handle_error(e, request)

    @post.route('/posts', methods=['GET'])
    @login_required
    def get_all_user_posts():
        try:
            limit = request.args.get('limit', 10)
            posts = Posts.query.filter_by(user_id=current_user.id).limit(limit).all()
            data = []
            for post in posts:
                comments = []
                for comment in post.comments:
                    comments.append({
                        'id': comment.id,
                        'text': comment.text,
                        'user_id': comment.user_id
                    })

                data.append({
                    'id': post.id,
                    'image': post.image_url,
                    'caption': post.caption,
                    'user_id': post.user_id,
                    'comments': comments,
                    'comments_count': len(post.comments)
                })
            return jsonify({
                'status': 'success',
                'data': data
            }), 200
        except Exception as e:
            handle_error(e, request)

    
    @post.route('/post/<int:post_id>/comments', methods=['GET'])
    def get_post_comments(post_id):
        try:
            post = Posts.query.filter_by(id=post_id).first()

            if not post:
                return jsonify({
                    'status': 'error',
                    'message': 'Post not found'
                }), 404
            
            data = []
            for comment in post.comments:
                data.append({
                    'id': comment.id,
                    'text': comment.text,
                    'user_id': comment.user_id
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
        
    @post.route('/post/delete/<int:post_id>', methods=['DELETE'])
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


    @post.route('/post/update/<int:post_id>', methods=['PUT'])
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

            args = request.get_json()
            image = args['image']
            caption = args['caption']
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