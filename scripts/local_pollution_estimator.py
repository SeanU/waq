### this code calculates the estimated pollution degree
### based on the data in our dataset

import datetime as dt
import numpy as np
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report, classification
from sklearn.ensemble import RandomForestClassifier

import calibration_function
import calibration_run

def estimated_pollution(pollutant, latitude, longitude, timedelta):
    ### for each pollutant, recall what model and parameter do we want to use
    mod = model_dictionary[pollutant]['model']
    acc = model_dictionary[pollutant]['accuracy']

    ### estimate the Warning Code
    level_pred = mod.predict([[latitude, longitude, timedelta]])

    if level_pred == 0:
        warning_level = 'Green'
    if level_pred == 1:
        warning_level = 'Amber'
    if level_pred == 2:
        warning_level = 'Red'

    print ('With ', "%0.2f" % (acc * 100 ), " probability, the warning level in your zone is: ", warning_level)

    return (warning_level, acc)
