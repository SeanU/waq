import dill

class MetaModel(object):

    # this store all of the fitted models in a single object
    # and will output predictions for a given lat, long, time, pollutant
    _models = {}
    _accuracies = {}

    def __init__(self, model_dictionary):
        for pollutant in model_dictionary:
            self._models[pollutant] = model_dictionary[pollutant]['model']
            self._accuracies[pollutant] = model_dictionary[pollutant]['accuracy']

    def __repr__(self):
        model_list_string = '\n ::'.join(
            ['Model '+'"'+k+'":: '+str(v.__class__).replace("'",'') 
                for k,v in self._models.items()])
        if model_list_string:
            model_list_string = '\n ::'+model_list_string
        return '<AllModels object at 0x{:x} with {} models>{}'.format(
            id(self), len(self._models), model_list_string)

    def estimated_pollution(self, latitude, longitude, timedelta=0, pollutants=None):
        ### estimate the Warning Code for each pollutant
        model_predictions = []
        for pollutant in self._models:
            level_pred = mod.predict([[latitude, longitude, timedelta]])
            acc = self._accuracies[pollutant]

            if level_pred == 0:
                warning_level = 'Green'
            if level_pred == 1:
                warning_level = 'Amber'
            if level_pred == 2:
                warning_level = 'Red'

            model_predictions.append([pollutant, acc, latitude, longitude, timedelta, level_pred])
        
        #instead of the print and return functions here
        #you should probably save the results in a df, array, csv etc to pass to the API
        #each model output needs to include [lat, long, date, pollutant, status, accuracy]
        #the entire output should be one file, array, etc
        print ('With ', "%0.2f" % (acc * 100 ), " probability, the warning level in your zone is: ", warning_level)
        return model_predictions

# create meta_model object and load in the model dictionary
meta_model = MetaModel(model_dictionary)

# pickle the model
with open('/path/to/file.pickle', 'wb') as fp:
    dill.dump(meta_model, fp)

# unpickle the model
with open('/path/to/file.pickle', 'rb') as fp:
    meta_model = dill.load(fp)
