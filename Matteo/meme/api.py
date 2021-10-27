from flask import Flask, request
from flask_restful import Resource, Api
from collectionM import CollectionMemes
from uuid import UUID
import validators

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

collectionMemes = CollectionMemes()

def validate_uuid(uuid_to_test, version=4):
    try:
        print('start test uuid')
        uuid_obj = UUID(uuid_to_test,version=version)
        print('test uuid: valid')
    except ValueError:
        print('test uuid: fail')
        return False
    return str(uuid_obj)==uuid_to_test

class MemesColl(Resource):
    def get(self, memeid):
        if not validate_uuid(memeid):
            return {'Error':'uuid not valid'}, 404
        
        attributes = collectionMemes.get_meme(memeid)
        
        if attributes is None:
            return None, 404

        return attributes, 200
        

    def post(self, memeid):
        if not validate_uuid(memeid):
            return {'Error':'uuid not valid'}, 400
        
        if not request.is_json:
            return None, 400

        data = request.get_json()

        if 'title' not in data:
            return None, 400
        else:
            if len(data['title']) > 100:
                return None, 400

        if 'link' not in data:
            return None, 400
        else:
            if not validators.url(data['link']):
                return None, 400

        if 'tags' not in data:
            return None, 400
        else:
            if len(data['tags']) < 2:
                return None, 400
            else:
                for tag in data['tags']:
                    if len(tag) < 3 or len(tag) > 30:
                        return None, 400
        
        media_val = ["image", "video"]
        if 'media' not in data:
            return None, 400
        else:
            if data['media'] not in media_val:
                return None, 400

        result = collectionMemes.insert_meme(memeid, data)

        if result == False:
            return None, 409

        return None, 201


class MemesByTag(Resource):
    def get(self, tag):
        if len(tag) < 3 or len(tag) > 30:
            return None, 406
        lista = collectionMemes.get_meme_by_tag(tag)
        return lista, 202

api.add_resource(MemesColl, f'{basePath}/meme/<string:memeid>')
api.add_resource(MemesByTag, f'{basePath}/memesByTag/<string:tag>')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
