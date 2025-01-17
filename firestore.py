import firebase_admin
from firebase_admin import firestore, credentials
from config import GOOGLE_APPLICATION_CREDENTIALS

cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()
