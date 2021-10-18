from google.cloud import firestore

#dal file open api metto a posto la classe che rappresenta la risorsa
#gli attributi servono per avere dei valori di default a scopo di test
#prendo le variabili dell'url dell'API e le metto come parametri della get e post della classe
#creo le query per firestore

class Marketplace(object):
    def __init__(self):
        self.db = firestore.Client()
        self.title = "Star Wars Jedi: Fallen Order"
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
            'price': kwargs.get('price', self.price)
        })
        return 'ok'
    
    def update_price(self, user, game, newPrice):
        try:
            ref = self.db.collection(f'{user}').document(f'{game}').get()
            if ref.exists:
                pass
        except ValueError:
            print('Error: valueError')
            return None
        ref = self.db.collection(f'{user}').document(f'{game}')
        oldPrice = ref.get().to_dict()['price']
        print(oldPrice)
        if newPrice < oldPrice:
            self.db.collection(f'{user}').document(f'{game}').update({'price': newPrice})
            return 'ok'
        else:
            return None