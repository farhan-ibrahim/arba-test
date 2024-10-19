# Get data from sqlite database
# Transfer to firebase firestore
from app.models import Comments, Posts, Users
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import app

cred = credentials.Certificate('./arba-test-bf431-e6e6d5989489.json')
firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()

limit = 10

with app.create_app().app_context():
    users = Users.query.limit(limit).all()
    for user in users:
        print(user.name, user.email)

        db.collection('users').document(str(user.id)).set({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'password': user.password,
        })

        print(f'Added {len(users)} users added to firestore')


    posts = Posts.query.limit(limit).all()
    for post in posts:
        print(post.caption, post.image_url)

        db.collection('posts').document(str(post.id)).set({
            'id': post.id,
            'caption': post.caption,
            'image_url': post.image_url,
            'user_id': post.user_id,
        })

        print(f'Added {len(posts)} posts added to firestore')

    comments = Comments.query.limit(limit).all()
    for comment in comments:
        print(comment.text)

        db.collection('comments').document(str(comment.id)).set({
            'id': comment.id,
            'text': comment.text,
            'user_id': comment.user_id,
            'post_id': comment.post_id,
        })

        print(f'Added {len(comments)} comments added to firestore')


