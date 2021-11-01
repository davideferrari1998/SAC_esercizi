from flask import Flask, request
from flask_restful import Resource, Api
from travels import Travel__database
from uuid import UUID
import datetime
import json


app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

travel__database = Travel__database()

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    return True

def validate_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test,version=version)
    except ValueError:
        return False
    return str(uuid_obj)==uuid_to_test

class Travels(Resource):
    def get(self, user, date):

        if not validate_uuid(user) or not validate(date):
            return {'ERROR':'USER UUID OR DATE NOT VALID'},404

        result = travel__database.get_travel(user, date)

        if result is None:
            return {'OUTPUT':'TRAVEL NOT FOUND'},404

        return result, 200

    def post(self, user, date):
        
        #Valido user e date
        if not validate_uuid(user) or not validate(date):
            return {'ERROR':'USER UUID OR DATE NOT VALID'},400
        #Controllo che il payload sia in json
        if not request.is_json:
            return {'ERROR':'JSON'},400
        
        #Ottengo il payload
        json = request.get_json()
        

        #INPUT REQUIRED PER 'from' e 'to'

        if 'from' not in json or 'to' not in json:
            return {'ERROR':'JSON'},400

        #Prendo i valori esistenti

        dep = json['from']
        dest = json['to']

        #verifico che siano corretti

        if len(dep) != 3 or len(dest) != 3:
            return {'ERROR':'DEPARTURE OR DESTINATION ARE INVALID'},400

        #Controllo che il viaggio non sia già presente
        duplicate = travel__database.get_travel(user, date)
        if duplicate is not None:
            return {'ERROR':'Travel already in DATABASE'},409
        
        if travel__database.insert_travel(user, date, **json) == 'ok':
            return None,201

        return {'ERROR':'Problem with Database'},400

class Travels_Friends(Resource):
    def get(self, user):

        if not validate_uuid(user):
            return {'ERROR':'USER UUID NOT VALID'},405

        result = travel__database.get_friends(user)

        if result == []:
            return {'OUTPUT':'There are not friends with travels correlated!'},405
        
        return result, 202

api.add_resource(Travels, f'{basePath}/travel/<string:user>/<string:date>')
api.add_resource(Travels_Friends, f'{basePath}/travel/friends/<string:user>')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
