from flask import Flask
from flask_restful import Resource, Api
from marketplace import Marketplace

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'

marketplace = Marketplace()

class VGMarketplace(Resource):
    def get(self):
        ...

    def post(self):
        ...


api.add_resource(VGMarketplace, f'{basePath}/')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
