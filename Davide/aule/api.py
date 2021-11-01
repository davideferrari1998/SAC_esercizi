from flask import Flask, request
from flask_restful import Resource, Api
from aule import Database_posti
from uuid import UUID
from google.cloud import firestore

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

aule_database = Database_posti()

def validate_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test,version=version)
    except ValueError:
        return False
    return str(uuid_obj)==uuid_to_test

class cleanDB(Resource):
    def get(self):
        db=firestore.Client()
        for collection in db.collections():
            for doc in collection.stream():
                doc.reference.delete()

        return "ok",200

class Seats(Resource):
    def get(self, course):
        
        seats = []

        if course not in ['A','B','C']:
            return {'ERROR':'INVALID COURSE'}, 405
        
        col = "Course" + course
        db=firestore.Client()
        ref = db.collection(col)
        for r in ref.stream():
            posto = r.to_dict()
            seats.append(posto['seat'])
        
        ret = {'seat': seats}
        return ret, 202

class Aule_Api(Resource):
    def get(self, student):
        if not validate_uuid(student):
            return {'ERROR':'INVALID STUDENT ID'}, 404

        ret = aule_database.get_student_seats(student)

        return ret, 200

    def post(self, student):
        
        if not validate_uuid(student):
            return {'ERROR':'INVALID STUDENT ID'}, 400
        
        #Controllo che il payload sia in json
        if not request.is_json:
            return {'ERROR':'JSON'},400

        #Ottengo il payload
        json = request.get_json()

        #INPUT REQUIRED 

        if 'courses' not in json: 
            return {'ERROR':'JSON'},400

        corsi = json['courses']

        #Controllo elementi del vettore

        for i in corsi:
            if i != 'A' and i != 'B' and i != 'C':
                 return {'ERROR':'NOT VALID COURSES'},400

        ret = { "reservations" : []}
        for i in corsi:
            ret_val = aule_database.insert_student_seat(student, i)

            if ret_val == 1:
                return {'Conflict':'Seat already prenoted for student {} in course {}'.format(student,i)},409

            if ret_val == 2:
                return {'Error':'No more seats available in course {}'.format(i)},412
            
            j = {'seat': ret_val}
            j['course'] = i
            ret['reservations'].append(j)
        
        return ret,201


api.add_resource(Aule_Api, f'{basePath}/courses/<string:student>')
api.add_resource(Seats, f'{basePath}/seats/<string:course>')
api.add_resource(cleanDB, f'{basePath}/clean')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
