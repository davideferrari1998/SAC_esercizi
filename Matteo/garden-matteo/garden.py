from google.cloud import firestore

class Garden(object):
    def __init__(self):
        self.db = firestore.Client()

    def get_info_semina(self, date, plant):
        ref = self.db.collection(date).document(plant).get()
        if ref.exists:
            return ref.to_dict()
        return None

    def insert_method(self, date, plant, data):
        ref = self.db.collection(date).document(plant).get()
        if ref.exists:
            return False
        self.db.collection(date).document(plant).set(data)
        return True

    def get_plant_details(self, plant):
        ref = self.db.collections()
        for collection in ref:
            for doc in collection.stream():
                if plant == doc.to_dict()["plant"]["name"]:
                    return doc.to_dict()["plant"]
        return None