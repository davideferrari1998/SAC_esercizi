from google.cloud import firestore

class Aula(object):

    riga = 'A'
    posto = 1
    capienza = 0
    id = ""

    def __init__(self, id):
        self.id = id
        self.db = firestore.Client()
        course = 'Course' + id
        for user in self.db.collection(course).stream():
            self.capienza = self.capienza + 1

    def get_posto(self):
        if self.capienza == 0:
            self.capienza = self.capienza + 1
            self.posto = 1
            self.riga = 'A'
            return f'{self.riga}{self.posto}'

        if self.capienza == 40:
            return None

        if ord(self.riga) % 2 != 0:
            if self.posto <= 7:
                self.posto = self.posto + 2
            else:
                self.posto = 2
                self.riga = chr(ord(self.riga) + 1)
        else:
            if self.posto <= 8:
                self.posto = self.posto + 2
            else:
                self.posto = 1
                self.riga = chr(ord(self.riga) + 1)

        self.capienza = self.capienza + 1
        return f'{self.riga}{self.posto}'

    
class Database_posti(object):
    def __init__(self):
        self.db = firestore.Client()
        self.courseA = Aula('A')
        self.courseB = Aula('B')
        self.courseC = Aula('C')


    def get_student_seats(self, student_id):
        
        ret_val = { "reservations": []}
        
        refA = self.db.collection('CourseA').document(f'{student_id}').get()
        if refA.exists:
            resA = refA.to_dict()
            resA['course'] = "A"
            ret_val['reservations'].append(resA)

        refB = self.db.collection('CourseB').document(f'{student_id}').get()
        if refB.exists:
            resB = refB.to_dict()
            resB['course'] = "B"
            ret_val['reservations'].append(resB)

        refC = self.db.collection('CourseC').document(f'{student_id}').get()
        if refC.exists:
            resC = refC.to_dict()
            resC['course'] = "C"
            ret_val['reservations'].append(resC)

        return ret_val


    def insert_student_seat(self, student_id, course):
    
        if course == 'A':
            ref = self.db.collection('CourseA').document(f'{student_id}').get()
            if ref.exists:
                return 1
            r = self.db.collection('CourseA').document(f'{student_id}')
            posto = self.courseA.get_posto()
        
        if course == 'B':
            ref = self.db.collection('CourseB').document(f'{student_id}').get()
            if ref.exists:
                return 1
            r = self.db.collection('CourseB').document(f'{student_id}')
            posto = self.courseB.get_posto()
        
        if course == 'C':
            ref = self.db.collection('CourseC').document(f'{student_id}').get()
            if ref.exists:
                return 1
            r = self.db.collection('CourseC').document(f'{student_id}')
            posto = self.courseC.get_posto()

        if posto == None:
            return 2

        r.set({'seat': posto})

        return posto
        