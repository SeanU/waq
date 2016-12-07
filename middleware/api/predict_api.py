from flask import Flask
from flask import request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class PredictFlag(Resource):
    def get(self):
        contaminant_type = request.args.get('type')
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        if(contaminant_type and lat and lng):
            return {'contaminant_type': contaminant_type, 'lat': lat, 'lng': lng}
        else:
            return {'Error': 'Insufficient parameters passed.'}, 400

api.add_resource(PredictFlag, '/getPrediction')

if __name__ == '__main__':
    app.run(debug=True)
