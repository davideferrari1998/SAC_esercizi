from google.cloud import firestore

class Meme_database(object):
    def __init__(self):
        self.db = firestore.Client()

    def get_meme(self, meme_id):
        try:
            ref = self.db.collection('meme').document(f'{meme_id}').get()
            if ref.exists:
                return ref.to_dict()
        except:
            return False


    def insert_meme(self, meme_id, **kwargs):
        
        try:
            ref = self.db.collection('meme').document(f'{meme_id}')
            ref.set({
                'title': kwargs.get('title'),
                'link': kwargs.get('link'),
                'media': kwargs.get('media'),
                'tags': kwargs.get('tags')
            })
            return True
        except:
            return False