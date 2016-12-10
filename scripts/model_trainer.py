### this code calibrates the optimal contaminant estimator
### for any contaminant

import datetime as dt
import numpy as np
import pandas as pd
import re
import dill

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# map from status to number
def convert_status(level):
    if (level == 'green'):
        return 0
    if (level == 'amber'):
        return 1    
    if (level =='red'):
        return 2
    else:
        return -1

# load and do a final cleaning on the data
def load_data(file_path):
    type_dict = {'site_id': str, 
                'site_name': str, 
                'state_id': int, 
                'state_name': str, 
                'contaminant_type': str, 
                'measurement_date': str, 
                'measurement_time': str, 
                'contaminant_cat': str, 
                'contaminant': str, 
                'value': str, 
                'status': str, 
                'rank': int, 
                'code': int, 
                'lat': float, 
                'lng': float}

    df = pd.read_csv('water-data.csv', dtype=type_dict)
    # clean up any remaining greater-then or less-than chars in value column
    df['imputed_value'] = (df.value
                             .str.replace(r'[<>,]','')
                             .str.replace(r'nd|not detected|absen.*','0', case=False))

    need_fix = df.imputed_value[
                    df.imputed_value.str.match(r'(\d+\.?\d*)\-\d+', as_indexer=True)
                    ]
    
    df.imputed_value[need_fix.index] = need_fix.apply(lambda x: re.sub(r'(\d+\.?\d*)\-\d+', r'\1', x))
    df.imputed_value = df.imputed_value.astype(float)
    # remove unusual dates > 2016
    df = (df[df.measurement_date.apply(lambda x: x[:4]).astype(int)<=dt.datetime.now().year]
            .reset_index(drop=True))

    # convert date and time from strings
    df['measurement_date'] = pd.to_datetime(df.measurement_date)
    df['measurement_time'] = pd.to_datetime(df.measurement_time).dt.time
    df['time_delta'] = (dt.datetime.now().date() - df.measurement_date).apply(lambda x: x.days)
    df['status_numeric'] = df.status.apply(convert_status)
    return df

#break into training and test
def splitData(df, id_col='site_id', train_fraction=0.8):
    # check how many unique sites we are measureing this contaminant at
    numLocations = df[id_col].unique().size
    
    # pull out randomly selected entire location ids for the test set
    trainLocations = np.random.choice(df[id_col].unique(), 
        int(train_fraction*numLocations), replace = False)
    testLocations = np.setdiff1d(df[id_col].unique(), trainLocations)

    # subset the data using the train and test location identifiers
    train_data = df[df[id_col].isin(trainLocations)]
    test_data = df[df[id_col].isin(testLocations)]

    return train_data, test_data

def find_best_model(df, contaminant, verbose=False):
    train_data, test_data = splitData(df[df.contaminant==contaminant])

    ### make sure the values make sense:
    if verbose:
        print('Contaminant ', contaminant)
        print('Status Levels: ', df.status.unique() )
        print('Status Codes: ', df.status_numeric.unique() )
        print('train data sample size', train_data.size)
        print('test data sample size', test_data.size)
    
    train_labels = train_data.status_numeric

    # create model templates
    RF = RandomForestClassifier()
    kNN = KNeighborsClassifier()

    kNN_scores = []
    RF_scores = []
    for p in range(2,100):
        kNN.n_neighbors = p
        RF.n_estimators = p

        kNN.fit(X=train_data[['lat', 'lng', 'time_delta']],
                y=train_data.status_numeric)
        kNN_scores.append((p, kNN.score(X=test_data[['lat', 'lng', 'time_delta']],
                                  y=test_data.status_numeric)))

        RF.fit(X=train_data[['lat', 'lng', 'time_delta']].astype(int),
               y=train_data.status_numeric)
        RF_scores.append((p, RF.score(X=test_data[['lat', 'lng', 'time_delta']].astype(int),
                                        y=test_data.status_numeric)))

    # find the most accurate model and parameter
    if max(kNN_scores, key = lambda x: x[1])[1] > max(RF_scores, key = lambda x: x[1])[1]:
        return contaminant, "KNN", max(kNN_scores, key = lambda x: x[1])
    else:
        return contaminant, "RF", max(RF_scores, key = lambda x: x[1])


def create_model_dict(df, verbose=False):
    model_dict = {}
    for c in df.contaminant.unique():
        contaminant, model_type, (param, acc) = find_best_model(df, c)
        full_train= df[df.contaminant==c]
        if model_type == 'kNN':
            model = KNeighborsClassifier(param)
            model.fit(X = full_train[['lat', 'lng', 'time_delta']], y = full_train.status_numeric)
        elif model_type == 'RF':
            model = RandomForestClassifier(param)
            model.fit(X = full_train[['lat', 'lng', 'time_delta']].astype(int), y = full_train.status_numeric)
        model_dict[contaminant] = {'model': model, 'accuracy':acc}
    return model_dict



class MetaModel(object):

    # this store all of the fitted models in a single object
    # and will output predictions for a given lat, long, time, contaminant
    _models = {}
    _accuracies = {}

    def __init__(self, model_dictionary):
        for contaminant in model_dictionary:
            self._models[contaminant] = model_dictionary[contaminant]['model']
            self._accuracies[contaminant] = model_dictionary[contaminant]['accuracy']

    def __repr__(self):
        model_list_string = '\n ::'.join(
            ['Model '+'"'+k+'":: '+str(v.__class__).replace("'",'') 
                for k,v in self._models.items()])
        if model_list_string:
            model_list_string = '\n ::'+model_list_string
        return '<AllModels object at 0x{:x} with {} models>{}'.format(
            id(self), len(self._models), model_list_string)

    def estimated_pollution(self, latitude, longitude, timedelta=0):
        ### estimate the Warning Code for each contaminant
        model_predictions = [['contaminant','status','accuracy','lat','lng','time_delta']]
        for contaminant in self._models:
            level_pred = _models[contaminant].predict([[latitude, longitude, timedelta]])
            acc = self._accuracies[contaminant]

            if level_pred == 0:
                status = 'Green'
            if level_pred == 1:
                status = 'Amber'
            if level_pred == 2:
                status = 'Red'

            model_predictions.append([contaminant, status, acc, latitude, longitude, timedelta])
        
        #this return function returns a list of list
        #we may want to save the results in a df, csv etc to pass to the API
        return model_predictions

    def to_pickle(self, file_path):
        with open(file_path, 'wb') as fp:
            dill.dump(self, fp)


# load the data and run the trainers
df = load_data('water-data.csv')
trained_models = create_model_dict(df)


# create meta_model object and load in the model dictionary
meta_model = MetaModel(trained_models)

# save the models
meta_model.to_pickle('trained_models.pickle')


