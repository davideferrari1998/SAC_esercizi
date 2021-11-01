from flask import Flask, request
from flask_restful import Resource, Api
from meme import Meme_database
from uuid import UUID
import validators

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

meme_database = Meme_database()

def validate_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test,version=version)
    except ValueError:
        return False
    return str(uuid_obj)==uuid_to_test

class Meme(Resource):
    def get(self, memeid):
        if not validate_uuid(memeid):
            return {'ERROR':'INVALID MEME ID'}, 404

        result = meme_database.get_meme(memeid)

        if result is None:
            return {'OUTPUT':'No MEME FOUND'},404

        return result,200

    def post(self, memeid):

        if not validate_uuid(memeid):
            return {'ERROR':'INVALID MEME ID'}, 400
        
        
        #Controllo che il payload sia in json
        if not request.is_json:
            return {'ERROR':'JSON'},400
        
        #Ottengo il payload
        json = request.get_json()
        
        #INPUT REQUIRED 

        if 'title' not in json or 'link' not in json or 'media' not in json or 'tags' not in json:
            return {'ERROR':'JSON'},400
        
        #Ottengo i campi
        tags = []
        title = json['title']
        link = json['link']
        media = json['media']
        tags = json['tags']

        #Verifico validità dei campi
        if len(title) > 100:
            return {'ERROR':'JSON TITLE'},400

        if media not in ['image', 'video']:
            return {'ERROR':'JSON MEDIA'},400

        #Controllo che tags sia una stringa
        if not isinstance(tags, list):
            return {'ERROR':'JSON TAGS NOT A LIST'},400

        if len(tags) < 2:
            return {'ERROR':'JSON TAGS NUMBER'},400

        for i in tags:
            if len(i) < 3 or len(i) > 30:
                return {'ERROR':'JSON TAGS LENGTH'},400

        #Controllo per URL
        if not validators.url(link):
            return {'ERROR':'JSON LINK'},400

        #Controllo che il MEME non esista già
        duplicate = meme_database.get_meme(memeid)
        if duplicate is not None:
            return {'ERROR':'MEME already in DATABASE'},409

        if meme_database.insert_meme(memeid, **json):
            return None, 201

        return {'ERROR':'Problem with Database'},400



api.add_resource(Meme, f'{basePath}/meme/<string:memeid>')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
