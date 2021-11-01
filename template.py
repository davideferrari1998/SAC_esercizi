
#-------------- VALIDAZIONE UUID --------------

from uuid import UUID

def validate_uuid(uuid_to_test, version=4):
    try:
        print('start test uuid')
        uuid_obj = UUID(uuid_to_test,version=version)
        print('test uuid: valid')
    except ValueError:
        print('test uuid: fail')
        return False
    return str(uuid_obj)==uuid_to_test


#-------------- VALIDAZIONE DATA --------------

import datetime

def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    return True

#-------------- API POST TEMPLATE --------------

def post(self, user, date):
        if not validate_uuid(user):
            return {'Error':'uuid not valid'}, 404 

        if not validate_date(date):
            return {'Error':'date not valid, should be YYYY-MM-DD'}, 404

        if not request.is_json:
            return None, 400

        data = request.get_json()

        #verifica presenza dei campi

        if 'field' not in data:
            return {"Error": "Field doesn't exists."}, 400

        field = data['field']

        #ripeti per altri campi


        return {"msg":"Success."}, 201

#-------------- main.py TEMPLATE --------------

from flask import Flask, render_template
from google.cloud import firestore

app = Flask(__name__)

db = firestore.Client()

@app.route('/', methods=['GET'])
def main_page():
    ...

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)


#-------------- api.py TEMPLATE --------------

from flask import Flask, request
from flask_restful import Resource, Api
#import la classe che gestisce la risorsa
#from garden import Garden

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

#garden = Garden()

#classe di esempio
class GardenResource(Resource):
    def get(self, date, plant):
        ...

    def post(self, date, plant):
        ...

#cambia url finale a seconda della specifica
api.add_resource(GardenResource, f'{basePath}/garden/plant/<string:date>/<string:plant>')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
