from google.cloud import firestore

class Marketplace(object):
    def __init__(self):
        self.db = firestore.Client()
        self.title= "Star Wars: Jedi Fallen Order"
        self.year = 2019
        self.console = "ps4"
        self.price = "35.00"



    def get_videogame(self, user, game):
        try:
            ref = self.db.collection(f'{user}').document(f'{game}').get()
            if ref.exists:
                return ref.to_dict()
        except ValueError:
                return None


    def insert_videogame(self, user, game, **kwargs):
        ref = self.db.collection(f'{user}').document(f'{game}')
        ref.set({
            'title': kwargs.get('title', self.title),
            'year': kwargs.get('year', self.year),
            'console': kwargs.get('console', self.console),
            'price': kwargs.get('price', self.price),
        })
        return 'ok'


    def update_price(self, user, game, newprice):
        try:
            ref = self.db.collection(f'{user}').document(f'{game}').get()
            if ref.exists:
                pass
        except ValueError:
                return None
        
        ref = self.db.collection(f'{user}').document(f'{game}')
        oldprice = ref.get().to_dict()['price']
        if newprice < oldprice:
            self.db.collection(f'{user}').document(f'{game}').update({'price':newprice})
            return 'ok'
        else:
            return None
        