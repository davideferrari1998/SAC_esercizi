from google.cloud import firestore

class Garden_Database(object):
    def __init__(self):
        self.db = firestore.Client()

    def get_plant(self, date, plant):
        try:
            ref = self.db.collection(f'{date}').document(f'{plant}').get()
            if ref.exists:
                return ref.to_dict()
        except ValueError:
            return None

    def insert_plant(self, date, plant, body):
        
        ref = self.db.collection(f'{date}').document(f'{plant}')
        ref.set({
            'plant' : {
                'name' : body['plant']['name'],
                'sprout-time': body['plant']['sprout-time'],
                'full-growth': body['plant']['full-growth'],
                'edible' : body['plant']['edible']
            },
            'num' : body['num']
        })
        return 'ok'

    def get_plant_details(self, plant):
        
        for col in self.db.collections():
            for doc in col.stream():
                if doc.id == plant:
                    return doc.to_dict()["plant"]

        
