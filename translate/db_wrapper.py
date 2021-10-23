
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class DatabaseWrapper:
    database = None
    def __init__(self):
        if self.database is None:
            cred = credentials.Certificate("key.json")
            firebase_admin.initialize_app(cred)
            self.database = firestore.client()
        self.__status_reference = self.database.collection('status')
    
    def get_status(self, document_id:str) -> dict:
        resp = self.__status_reference.document(document_id).get()
        # TODO: response check
        return resp.to_dict()
