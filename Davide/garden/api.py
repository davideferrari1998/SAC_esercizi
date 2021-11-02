from flask import Flask, request
from flask_restful import Resource, Api
from garden import Garden_Database
import datetime

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

garden_database = Garden_Database()

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d-%m-%Y')
    except ValueError:
        return False
    return True

class Garden_api(Resource):
    def get(self, date, plant):

        if not validate(date):
            return {'ERROR':'DATE NOT VALID'},404

        if len(plant) < 3 or len(plant) > 30:
            return {'ERROR':'PLANT NOT VALID'},404
        
        res = garden_database.get_plant(date, plant)

        if res is None:
            return {'OUTPUT':'PLANT NOT FOUND'},404

        return res, 200

    def post(self, date, plant):

        if not validate(date):
            return {'ERROR':'DATE NOT VALID'},400

        if len(plant) < 3 or len(plant) > 30:
            return {'ERROR':'PLANT NOT VALID'},400

        #Controllo che il payload sia in json
        if not request.is_json:
            return {'ERROR':'JSON'},400
        
        json = request.get_json()

         #INPUT REQUIRED PER 'from' e 'to'

        if 'plant' not in json or 'num' not in json:
            return {'ERROR':'JSON'},400

        if 'name' not in json['plant']:
            return {'ERROR':'JSON name'},400
        
        if 'sprout-time' not in json['plant']:
            return {'ERROR':'JSON sprout-time'},400
            
        if 'full-growth' not in json['plant']:
            return {'ERROR':'JSON full-growth'},400

        if 'edible' not in json['plant']:
            return {'ERROR':'JSON edible'},400

        #Prendo i valori esistenti

        p = json['plant']

        if len(p['name']) < 3:
              return {'ERROR':'JSON NAME LENGTH'},400

        if len(p['sprout-time']) < 5:
              return {'ERROR':'JSON sprout-time LENGTH'},400

        if len(p['full-growth']) < 5:
              return {'ERROR':'JSON full-growth LENGTH'},400
        
        if p['edible'] != True and p['edible'] != False:
            return {'ERROR':'JSON EDIBLE NOT BOOLEAN'},400

        if not isinstance(json['num'], int):
            return {'ERROR':'JSON NUM NOT AN INTEGER'},400

        if json['num'] < 1:
            return {'ERROR':'JSON NUM'},400

        #CONTROLLO DUPLICATI

        dup = garden_database.get_plant(date, plant)
        if dup is not None:
            return {'ERROR':'Plant already in DATABASE'},409

        #Inserisco la pianta

        if garden_database.insert_plant(date, plant, json) == 'ok':
            return None, 201
        
        return {'ERROR':'ERROR WITH DATABASE'},400


class Garden_api_details(Resource):
    def get(self, plant):
        if len(plant) < 3 or len(plant) > 30:
            return {'ERROR':'PLANT NOT VALID'},405

        res = garden_database.get_plant_details(plant)

        if res is None:
            return {'OUTPUT':'PLANT NOT FOUND'},405

        return res, 202


api.add_resource(Garden_api, f'{basePath}/garden/plant/<string:date>/<string:plant>')
api.add_resource(Garden_api_details, f'{basePath}/plant/<string:plant>')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
