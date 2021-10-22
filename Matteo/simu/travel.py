from google.cloud import firestore
import datetime

class Itinerary(object):
    def __init__(self):
        self.db = firestore.Client()

    def get_itinerary(self, user, date):
        ref = self.db.collection('users').document(user).collection('travels')
        travels = []
        for travel in ref.stream():
            if travel.to_dict()['date'] == date:
                dict = travel.to_dict()
                del dict['date']
                travels.append(dict)
        if len(travels) == 0:
            return None
        else:
            return travels

    def insert_itinerary(self, user, date, data):
        ref = self.db.collection('users').document(user).collection('travels')
        for travel in ref.stream():
            if travel.to_dict()['date'] == date and travel.to_dict()['from'] == data['from'] and travel.to_dict()['to'] == data['to']:
                return False
        self.db.collection('users').document(user).set({'name':""})
        data['date'] = date
        print(data)
        ref.document().set(data)
        return True

    def get_friends(self, user, date):
        friends = []
        ref_utente1 = self.db.collection('users').document(user).collection('travels')
        info_utente1 = {}
        for travel in ref_utente1.stream():
            if travel.to_dict()['date'] == date:
                info_utente1 = travel.to_dict()
                break
        if 'from' not in info_utente1:
              return None

        ref = self.db.collection('users').stream()
        yesterday = datetime.datetime.strptime(info_utente1['date'], '%Y-%m-%d') - datetime.timedelta(days=1)
        tomorrow = datetime.datetime.strptime(info_utente1['date'], '%Y-%m-%d') + datetime.timedelta(days=1)
        actual_date = datetime.datetime.strptime(info_utente1['date'], '%Y-%m-%d')
        for user_uuid in ref:
            if user_uuid.id == user:
                print("stesso user")
                continue

            travels_ref = user_uuid.reference.collection('travels')
            for travel in travels_ref.stream():
                info = travel.to_dict()
            
                print("\n")
                print(info_utente1)
                print(info)
                print("\n")
                if info['from'] == info_utente1['from'] and info['to'] == info_utente1['to']:
                    if yesterday.strftime("%Y-%m-%d") == info['date'] or tomorrow.strftime("%Y-%m-%d") == info['date'] or actual_date == info['date']:
                        print('append')
                        if user_uuid.id not in friends:
                            friends.append(user_uuid.id)

        return friends