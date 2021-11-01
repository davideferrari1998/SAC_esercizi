from flask import Flask, request
from flask_restful import Resource, Api
from garden import Garden
import datetime

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

garden = Garden()

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    return True

class GardenResource(Resource):
    def get(self, date, plant):
        if not validate(date):
            return {"Error": "Generic error."}, 404
        
        if len(plant) < 3 or len(plant) > 20:
            return {"Error": "Generic error."}, 404

        data = garden.get_info_semina(date, plant)

        if data == None:
            return {"Error": "Generic error."}, 404

        return data, 200

    def post(self, date, plant):
        if not validate(date):
            return {"Error": "date not valid."}, 400
        
        if len(plant) < 3 or len(plant) > 20:
            return {"Error": "plant name not valid."}, 400

        if not request.is_json:
            return {"Error": "Request not json."}, 400

        data = request.get_json()

        if "plant" not in data:
             return {"Error": "plant not in data"}, 400
        
        if "num" not in data:
             return {"Error": "num not in data"}, 400
        
        plant_details = data["plant"]
        
        num = data["num"]

        if num < 1:
            return {"Error": "num not valid."}, 400

        if "name" not in plant_details or "sprout-time" not in plant_details or "full-growth" not in plant_details or "edible" not in plant_details:
            return {"Error": "Generic error."}, 400

        if len(plant_details["name"]) < 3:
            return {"Error": "name < 3 !"}, 400
        
        if len(plant_details["sprout-time"]) < 5:
            return {"Error": "sprout-time < 5 !"}, 400

        if len(plant_details["full-growth"]) < 5:
            return {"Error": "full-growth < 5 !"}, 400

        if plant_details['edible'] not in [True, False]:
            return {"Error": "edible field not bool!"}, 400

        res = garden.insert_method(date, plant, data)

        if not res:
            return {"Error": "Conflict. The user has already planted a similar plant on the same date"}, 409
        
        return {"msg":"Success."}, 201

class PlantDetails(Resource):
    def get(self, plant):
        if len(plant) < 3 or len(plant) > 20:
            return {"Error": "plant name not valid."}, 412

        data = garden.get_plant_details(plant)

        if data is None:
            return {"Error": "Plant doesn't exist in db."}, 412
        
        return data

api.add_resource(GardenResource, f'{basePath}/garden/plant/<string:date>/<string:plant>')
api.add_resource(PlantDetails, f'{basePath}/plant/<string:plant>')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
