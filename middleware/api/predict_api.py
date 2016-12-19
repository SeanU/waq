import datetime as dt
import numpy as np
import pandas as pd
import re
import dill
import json
import flask as fl
from flask import Flask
from flask import request
from flask_restful import Resource, Api
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
api = Api(app)


meta_model = None
# to predict:
# unpickle the model
with open('../trained_models.pickle', 'rb') as fpw:
    meta_water_model = dill.load(fpw)

with open('../trained_models_air.pickle', 'rb') as fpa:
    meta_air_model = dill.load(fpa)

# call predict function, returns list of lists of predictions
# prediction_list = meta_model.estimated_pollution(lat, lng, time_delta=0)

class PredictFlag(Resource):
    def get(self):
        contaminant_type = request.args.get('type')
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        if(contaminant_type and lat and lng):
            #if(contaminant_type == 'Water'):
            prediction_list_1 = meta_water_model.estimated_pollution(lat, lng, timedelta=0)
            #elif(contaminant_type == 'Air'):
            prediction_list_2 = meta_air_model.estimated_pollution(lat, lng, timedelta=0)
            #print("Model Predicted")
            jsonObj = list()
            for pred in prediction_list_1:
                if (pred[0] != 'contaminant'):
                    x = {}
                    x['contaminant'] = pred[0]
                    x['status'] = pred[1].lower()
                    x['accuracy'] = pred[2]
                    jsonObj.append(x)
            for pred in prediction_list_2:
                if (pred[0] != 'contaminant'):
                    x = {}
                    x['contaminant'] = pred[0]
                    x['status'] = pred[1].lower()
                    x['accuracy'] = pred[2]
                    jsonObj.append(x)
            #print(jsonObj)
            #return {'contaminant_type': contaminant_type, 'lat': lat, 'lng': lng}
            #return json.dumps(jsonObj, sort_keys = True, indent = 4, ensure_ascii=False)
            return fl.jsonify(jsonObj)
        else:
            return {'Error': 'Insufficient parameters passed.'}, 400

api.add_resource(PredictFlag, '/getPrediction')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
