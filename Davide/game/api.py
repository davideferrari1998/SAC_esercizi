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
    title = fields.Str(required=True, validate= lambda x: len(x)<=100)
    year = fields.Int(required=True, validate= lambda x: 2010 <= x <= 2020)
    console = fields.Str(required=True, validate= lambda x: x in ['ps4', 'xbox1', 'switch'])
    price = fields.Float(required=True, validate= lambda x: x >= 0.01)

def validate_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test,version=version)
    except ValueError:
        return False
    return str(uuid_obj)==uuid_to_test

def validate_body(json):
    try:
        #ritorna l'oggetto passato se validato
        return VGSchema().load(json)
    except:
        return False

class VGMarketplace(Resource):
    def get(self, user, game):
        if not validate_uuid(user) or not validate_uuid(game):
            return {'ERROR':'USER UUID OR GAME UUID NOT VALID'},404

        result = marketplace.get_videogame(user, game)

        if result is None:
            return {'ERROR':'No game found'}, 404
        
        return result,200

    def post(self, user, game):
        if not validate_uuid(user) or not validate_uuid(game):
            return {'ERROR':'USER UUID OR GAME UUID NOT VALID'},400
        if not request.is_json:
            return {'ERROR':'JSON'},400
        
        json = request.get_json()
        body = validate_body(json)
        if not body:
            return {'ERROR':'JSON arguments are invalid'},400
        
        duplicate = marketplace.get_videogame(user, game)
        if duplicate is not None:
            return {'ERROR':'The game already exists'},409

        if marketplace.insert_videogame(user, game, **body) == 'ok':
            return None, 201
        
        return {'ERROR':'Problem with Database'},400


class VGMarketplaceUpdata(Resource):
    def post(self,user, game):
        if not validate_uuid(user) or not validate_uuid(game):
            return {'ERROR':'USER UUID OR GAME UUID NOT VALID'},405
        if not request.is_json:
            return {'ERROR':'JSON'},405
        
        json = request.get_json()
        newprice = json['newprice']
        if newprice < 0.01:
            return {'ERROR':'New price invalid'},405

        if marketplace.update_price(user, game, newprice) == 'ok':
            return {'SUCCESS':'Correct UPDATE'}, 202
        
        return {'ERROR':'Problem with Database'},405

api.add_resource(VGMarketplaceUpdata, f'{basePath}/game/<string:user>/<string:game>/update')
api.add_resource(VGMarketplace, f'{basePath}/game/<string:user>/<string:game>')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

# Esempi di UUID
# 80605cb7-4d2a-452d-995f-7bf7e7abc1cf
# 670b9562-b30d-52d5-b827-655787665500
# 550e8400-e29b-41d4-a716-446655440000
# 4d4a0a5c-b57b-4213-aa0d-f37ae9c10658

#77344974-06b7-4bef-a6f0-f7429987c64f
#369e733b-1d1b-461c-a6a0-6bdd74593fed

# 488a2bdc-f4fd-4ff1-9ac2-2ee211ca4be5
# a3544d5e-36c5-41ce-a32e-dd14a7b53db5