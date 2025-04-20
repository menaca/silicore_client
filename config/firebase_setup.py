import firebase_admin
import json
from firebase_admin import credentials, firestore

JSON_PATH = "serviceAccountKey.json"

with open(JSON_PATH, "r") as f:
    key_data = json.load(f)
    
if not firebase_admin._apps:
    cred = credentials.Certificate(JSON_PATH)  
    firebase_admin.initialize_app(cred)

db = firestore.client()

collection = db.collection("computers")





