from flask import Flask, request
from flask_restful import Resource, Api
from marketplace import Marketplace
from marshmallow import Schema, fields, ValidationError
from uuid import UUID

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

marketplace = Marketplace()

class VGSchema(Schema):
    title = fields.Str(required=True, validate=lambda x: len(x)<=100)
    year = fields.Int(required=True, validate=lambda x: 2010<=x<=2021)
    console = fields.Str(required=True, validate=lambda x: x in ['ps4', 'ps5','xbox_one','xbox_x','xbox_s'])
    price = fields.Float(required=True, validate=lambda x: x>0.01)

def validate_uuid(uuid_to_test, version=4):
    try:
        print('start test uuid')
        uuid_obj = UUID(uuid_to_test,version=version)
        print('test uuid: valid')
    except ValueError:
        print('test uuid: fail')
        return False
    return str(uuid_obj)==uuid_to_test

def validate_body(json):
    print(json)
    try:
        #ritorna l'oggetto passato se validato
        return VGSchema().load(json)
    except ValueError:
        print('body test not valid')
        return False

class VGMarketplace(Resource):
    def get(self, user, game):
        if not validate_uuid(user) or not validate_uuid(game):
            return {"Error":"Generic error."}, 404
        return_value = marketplace.get_videogame(user, game)
        if return_value is None:
            return {"Error":"Generic error."}, 404
        return return_value, 200

    def post(self, user, game):
        #testiamo prima i campi
        print('post function entered')
        if not validate_uuid(user) or not validate_uuid(game):
            return None, 400
        if not request.is_json:
            return None, 400 #il valore lo prendo a seconda della specifica 400, 401 ecc...
        json = request.get_json()
        body = validate_body(json)

        if not body:
            return None, 400
        
        print(body)

        return_value = marketplace.get_videogame(user, game)
        if return_value is not None:
            return {"Error":"Conflict. The user has already inserted a game with the same id."}, 409

        if marketplace.insert_videogame(user, game, **body) == "ok":
            return None, 201
        return None, 400

class VGMarketplaceUpdate(Resource):
    def post(self, user, game):
        print('update function entered')
        if not validate_uuid(user) or not validate_uuid(game):
            return None, 405
        print('uuids validated')
        if not request.is_json:
            return None, 405
        print('request is json: ok')
        json = request.get_json()
        print(json)
        newPrice = json['newPrice']
        if newPrice < 0.01:
            return None, 405
        print('new price ok')
        if marketplace.update_price(user, game, newPrice) == 'ok':
            return {'msg':'Success.'}, 202
        return None, 405


api.add_resource(VGMarketplace, f'{basePath}/game/<string:user>/<string:game>')
api.add_resource(VGMarketplaceUpdate, f'{basePath}/game/<string:user>/<string:game>/update')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
