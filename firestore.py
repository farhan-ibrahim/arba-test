import firebase_admin
from firebase_admin import firestore, credentials

cred = credentials.Certificate('./arba-test-bf431-e6e6d5989489.json')
firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()
