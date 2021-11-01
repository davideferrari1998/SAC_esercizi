from google.cloud import firestore

class Marketplace(object):
    def __init__(self):
        self.db = firestore.Client()

    def get_method(self):
        ...

    def insert_method(self):
        ...