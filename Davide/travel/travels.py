from google.cloud import firestore
import datetime

class Travel__database(object):
    def __init__(self):
        self.db = firestore.Client()
        self.departure = "BLQ"
        self.destination = "NYC"

    def get_travel(self, user, date):
        try:
            ref = self.db.collection(f'{user}').document(f'{date}').get()
            if ref.exists:
                return ref.to_dict()
        except ValueError:
            return None

    def insert_travel(self, user, date, **kwargs):

        ref = self.db.collection(f'{user}').document(f'{date}')
        ref.set({
            'from': kwargs.get('from', self.departure),
            'to': kwargs.get('to', self.destination)
        })
        return 'ok'

    def get_friends(self, user):
        friends = []
        users_travels = []

        #ottengo tutti i viaggi nel mio utente
        ref = self.db.collection(f'{user}')
        for travel in ref.stream():
            json = travel.to_dict()
            json['date'] = travel.id
            users_travels.append(json)
        
        #cerco gli utenti che hanno almeno un viaggio condiviso
        for person in self.db.collections():
            
            if person.id == user:
                continue 
            
            for t in person.stream():
                
                info = t.to_dict()
                info['date'] = t.id
                
                yesterday = datetime.datetime.strptime(info['date'], '%Y-%m-%d') - datetime.timedelta(days=1)
                tomorrow = datetime.datetime.strptime(info['date'], '%Y-%m-%d') + datetime.timedelta(days=1) 

                for x in users_travels:

                    if x['date'] == info['date'] or x['date'] == yesterday.strftime("%Y-%m-%d") or x['date'] == tomorrow.strftime("%Y-%m-%d"):
                        #continuo il controllo
                        if x['from'] == info['from'] and x['to'] == info['to']:
                            #aggiungo amico se non è già presente
                            if person.id not in friends:
                                friends.append(person.id)
            
        
        
        return friends
