import firebase_admin
from firebase_admin import firestore, credentials
from config import GOOGLE_APPLICATION_CREDENTIALS

# Uncomment to use a service account as credentials
# Require as service account json file

# cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)

# Use the default credentials
cred = credentials.ApplicationDefault()
firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()
