
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
progress_ref = db.collection('progress')
todo = progress_ref.document('sAtI5bVcqLfvGCVtPnOf').get()
todo = todo.to_dict()
print(todo)