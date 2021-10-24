''' Wrapper module around Firestore '''
import hashlib
from firebase_admin import firestore


class DatabaseWrapper:
    ''' Wrapping Firestore '''
    database = None

    def __init__(self):
        if self.database is None:
            self.database = firestore.client()
        self.__status_reference = self.database.collection('status')
        self.__pages_reference = self.database.collection('pages')

    def get_pages(self, document_id: str) -> dict:
        hash_value = hashlib.md5(document_id.encode('utf-8')).hexdigest()
        return self.__pages_reference.document(hash_value).get().to_dict()

    def set_pages(self, document_id: str, data: dict) -> None:
        hash_value = hashlib.md5(document_id.encode('utf-8')).hexdigest()
        ref = self.__pages_reference.document(hash_value)
        ref.set(data)

    def get_status(self, document_id: str) -> dict:
        hash_value = hashlib.md5(document_id.encode('utf-8')).hexdigest()
        return self.__status_reference.document(hash_value).get().to_dict()

    def set_status(self, document_id: str, data: dict) -> None:
        hash_value = hashlib.md5(document_id.encode('utf-8')).hexdigest()
        ref = self.__status_reference.document(hash_value)
        ref.set(data)

    def remove_document(self, document_id: str) -> None:
        hash_value = hashlib.md5(document_id.encode('utf-8')).hexdigest()
        self.__status_reference.document(hash_value).delete()
