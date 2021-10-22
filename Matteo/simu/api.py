from flask import Flask, request
from flask_restful import Resource, Api
from travel import Itinerary
import datetime
from uuid import UUID
import json

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

itinerary = Itinerary()

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    return True

def validate_uuid(uuid_to_test, version=4):
    try:
        print('start test uuid')
        uuid_obj = UUID(uuid_to_test,version=version)
        print('test uuid: valid')
    except ValueError:
        print('test uuid: fail')
        return False
    return str(uuid_obj)==uuid_to_test

class ItineraryClassApi(Resource):
    def get(self, user, date):
        if not validate_uuid(user):
            return {'Error':'uuid not valid'}, 404 

        if not validate(date):
            return {'Error':'date not valid, should be YYYY-MM-DD'}, 404

        travels = itinerary.get_itinerary(user, date)

        if travels is None:
            return None, 404
        return travels, 200

    def post(self, user, date):
        if not validate_uuid(user):
            return {'Error':'uuid not valid'}, 404 

        if not validate(date):
            return {'Error':'date not valid, should be YYYY-MM-DD'}, 404

        if not request.is_json:
            return None, 400
        
        data = request.get_json()

        if len(data['from']) != 3 and len(data['to']) != 3:
            return None, 400

        if itinerary.insert_itinerary(user, date, data):
            return None, 201
        return None, 409

class ItineraryFriends(Resource):
    def get(self, user, date):
        if not validate_uuid(user):
            return {'Error':'uuid not valid'}, 407 

        if not validate(date):
            return {'Error':'date not valid, should be YYYY-MM-DD'}, 407

        friends = itinerary.get_friends(user, date)

        if friends is None:
            return None, 407

        return friends, 202

api.add_resource(ItineraryClassApi, f'{basePath}/travel/<string:user>/<string:date>')
api.add_resource(ItineraryFriends, f'{basePath}/friends/<string:user>/<string:date>')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
