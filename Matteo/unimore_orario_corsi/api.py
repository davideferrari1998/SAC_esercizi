from flask import Flask, request
from flask_restful import Resource, Api
from reservation import Reservation
from uuid import UUID
from google.cloud import firestore

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

reservation = Reservation()

def validate_uuid(uuid_to_test, version=4):
    try:
        print('start test uuid')
        uuid_obj = UUID(uuid_to_test,version=version)
        print('test uuid: valid')
    except ValueError:
        print('test uuid: fail')
        return False
    return str(uuid_obj)==uuid_to_test

courses_list = ['A','B','C']

class cleanDB(Resource):
    def get(self):
        db = firestore.Client()
        for collection in db.collections():
            for doc in collection.stream():
                doc.reference.delete()
        return "ok", 200
class seatsManager(Resource):
    def get(self, course):
        if course not in courses_list:
            return {"Error":"Course code not in ['A','B','C']"}, 410
        
        seats_list = reservation.get_seats_status(course)

        ret_val = {
            "seats": seats_list
        }

        return ret_val, 202

class reservationManager(Resource):
    def get(self, student):
        if not validate_uuid(student):
            return {'Error':'uuid not valid'}, 404

        reservations = reservation.get_reservations(student)
        
        return reservations

        

    def post(self, student):
        if not validate_uuid(student):
            return {'Error':'uuid not valid'}, 400

        if not request.is_json:
            return None, 400

        data = request.get_json()

        courses = ['A','B','C']

        if 'courses' not in data:
            return None, 400

        corsi = data['courses']

        for id in corsi:
            if id not in courses:
                return None, 400

        ret_val = reservation.insert_reservations(student, corsi)

        if ret_val == 1:
            return {"Conflict": "The student has already a seat for the selected course."}, 409
        if ret_val == 2:
            return {"Error": "No more seats available"}, 412

        return ret_val, 201

api.add_resource(reservationManager, f'{basePath}/courses/<string:student>')
api.add_resource(seatsManager, f'{basePath}/seats/<string:course>')
api.add_resource(cleanDB, f'{basePath}/clean')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
