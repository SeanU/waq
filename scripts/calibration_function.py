### this code calibrates the optimal pollutant estimator
### for any pollutant

import datetime as dt
import numpy as np
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report, classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV

def best_params(data, pollutant):
    df = data[data.Pollutant == pol[i]]
    train_data, test_data = splitData(df)
    train_labels = train_data.WarningCode

    RF = RandomForestClassifier()
    kNN = KNeighborsClassifier()

    ### try nearest neighbors, as depending on the size of the sample
    train_points = len(train_data.index)
    #### use up to 200 nearest neighbors, if sample size permits
    size = min((train_points-5), 200)
    parameters_RF = [{"n_estimators": [k for k in range(2, size)]}]
    parameters_kNN = [{"n_neighbors": [l for l in range(2, size)]}]

    ### run the GridSearch on these functions
    clf_rf = GridSearchCV(RF, parameters_RF, scoring="accuracy")
    clf_knn = GridSearchCV(kNN, parameters_kNN, scoring="accuracy")

    rf_model = clf_rf.fit(X=train_data[['Latitude', 'Longitude', 'TimeDelta']], y=train_data.WarningCode)
    knn_model = clf_knn.fit(X=train_data[['Latitude', 'Longitude', 'TimeDelta']], y=train_data.WarningCode)

    ### find what are the best estimates from each
    best_estimator_rf = clf_rf.best_estimator_
    best_score_rf = clf_rf.best_score_
    best_params_rf = clf_rf.best_params_
    best_estimator_knn = clf_knn.best_estimator_
    best_score_knn = clf_knn.best_score_
    best_params_knn = clf_knn.best_params_

    ### if needed, print the results of each
    print ('Best hyperparameters: ')
    print ('RF: ', best_estimator_rf)
    print ('Best score: ', best_score_rf)
    print ('Parameters: ', str(best_params_rf))

    print ('kNN: ', best_estimator_knn)
    print ('Best score: ', best_score_knn)
    print ('Parameters: ', str(best_params_knn))

    ### select the model and the parameter with the best score

    if (best_score_rf > best_score_knn):
        model = rf_model
        parameter = best_estimator_rf
        accuracy = best_score_rf
    else:
        model = knn_model
        parameter = best_estimator_knn
        accuracy = best_score_knn
    return (model, parameter, accuracy)
