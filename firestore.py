import firebase_admin
from firebase_admin import firestore, credentials

cred = credentials.ApplicationDefault()
firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()
