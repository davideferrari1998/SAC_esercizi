from google.cloud import firestore


class Aula:
    riga = 'A'
    posto = 1
    capienza = 0
    id = ""


    def __init__(self, id):
        self.id = id
        db = firestore.Client()
        for user in db.collection(id).stream():
            self.capienza = self.capienza + 1

    def __str__(self):
     return f"riga: {self.riga}, posto: {self.posto}, capienza: {self.capienza}, id: {self.id}"

    def get_posto(self):
        if self.capienza == 0:
            self.posto = 1
            self.capienza+=1
            return f'{self.riga}{self.posto}'
        if self.capienza == 40:
            return None
        if ord(self.riga) % 2 != 0:
            if self.posto <= 7:
                self.posto+=2
            else:
                self.posto = 2
                self.riga = chr(ord(self.riga) + 1)
        else:
            if self.posto <= 8:
                self.posto+=2
            else:
                self.posto = 1
                self.riga = chr(ord(self.riga) + 1)
        self.capienza+=1
        return f'{self.riga}{self.posto}'

class Reservation(object):
    def __init__(self):
        self.db = firestore.Client()
        self.courseA = Aula('A')
        self.courseB = Aula('B')
        self.courseC = Aula('C')
    
    def get_course(self, id):
        if id == self.courseA.id:
            return self.courseA
        if id == self.courseB.id:
            return self.courseB
        if id == self.courseC.id:
            return self.courseC

    def get_reservations(self, student):
        ret_val = {"reservations": []}
        for collection in self.db.collections():
            for user in collection.stream():
                if user.id == student:
                    ret_val["reservations"].append(user.to_dict())
        return ret_val

    def insert_reservations(self, student, courses = []):
        ret_val = {"reservations": []}
        for course in courses:
            print(course)
            ref = self.db.collection(course).document(student).get()
            if ref.exists:
                return 1
            print(self.get_course(course))
            posto = self.get_course(course).get_posto()
            print(self.get_course(course))
            print(posto)
            if posto == None:
                return 2

            self.db.collection(course).document(student).set({"posto": posto})
            
            ret_val["reservations"].append({
                "course": course,
                "seat": posto
                })

        print(ret_val) 
        return ret_val

    def get_seats_status(self, course):
        print(course)
        ref = self.db.collection(course)
        posti = []
        for user in ref.stream():
            info = user.to_dict()
            posti.append(info['posto'])
        return posti