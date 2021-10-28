''' Wrapper module around Firestore '''
import hashlib
from firebase_admin import firestore
from firebase_admin import db


class DatabaseWrapper:
    ''' Wrapping Firestore '''
    database = None

    def __init__(self):
        if self.database is None:
            self.database = firestore.client()

    def get_pages(self, document_id: str) -> dict:
        # hash_value = hashlib.md5(document_id.encode('utf-8')).hexdigest()
        res = self.database.collection(document_id).stream()
        pages = {}
        for doc in res:
            doc = doc.to_dict()
            if doc is None:
                continue
            pages[doc['url']] = doc
        return pages

    def set_pages(self, document_id: str, data: dict) -> None:
        for c_data in data:
            hash_value = hashlib.md5(c_data.encode('utf-8')).hexdigest()
            ref = self.database.collection(document_id).document(hash_value)
            ref.set(data[c_data])

    def set_page(self, collection_id: str, document_id: str, data: dict) -> None:
        hash_value = hashlib.md5(document_id.encode('utf-8')).hexdigest()
        ref = self.database.collection(collection_id).document(hash_value)
        ref.set(data)

    def get_status(self, document_id: str) -> dict:
        hash_value = hashlib.md5(document_id.encode('utf-8')).hexdigest()
        res = self.database.collection('status').document(hash_value).get()
        if res.exists:
            return res.to_dict()
        return None

    def set_status(self, document_id: str, data: dict) -> None:
        hash_value = hashlib.md5(document_id.encode('utf-8')).hexdigest()
        ref = self.database.collection('status').document(hash_value)
        ref.set(data)
    
    def update_status(self, document_id: str, data: dict) -> None:
        hash_value = hashlib.md5(document_id.encode('utf-8')).hexdigest()
        ref = self.database.collection('status').document(hash_value)
        ref.update(data)


    def remove_status_document(self, document_id: str) -> None:
        hash_value = hashlib.md5(document_id.encode('utf-8')).hexdigest()
        self.database.collection('status').document(hash_value).delete()

    def remove_pages_document(self, collection_id: str) -> None:
        for ref in self.database.collection(collection_id).stream():
            ref.reference.delete()

