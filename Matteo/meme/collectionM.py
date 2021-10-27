from google.cloud import firestore
from Levenshtein import _levenshtein


def min_lev(elem, tag):
        tagsOfElem = elem['tags']
        distances = list(tagsOfElem)
        print(distances)
        distances.sort(key = lambda x: _levenshtein.distance(tag, x))
        
        print(distances[0])

        return distances[0]

class CollectionMemes(object):
    def __init__(self):
        self.db = firestore.Client()

    def get_meme(self, memeId):
        attributes = []
        ref = self.db.collection(memeId).stream()
        for attribute in ref:
            attributes.append(attribute.to_dict())
        if len(attributes) == 0:
            return None
        return attributes
        
    def insert_meme(self, memeId, data):
        if len(self.db.collection(memeId).get()) != 0:
            return False

        ref = self.db.collection(memeId).document().set({
            'title': data['title'],
            'link': data['link'],
            'media': data['media'],
            'tags': data['tags']
        })

        return True

    def get_meme_by_tag(self, tag):

        lista = []
        for coll in self.db.collections():
            for doc in coll.stream():
                info = doc.to_dict()
                lista.append(info)
        lista.sort(key=lambda x: _levenshtein.distance(tag, min_lev(x, tag)))
        print(lista)
        
        return lista[0:5]