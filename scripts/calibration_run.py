### this code runs the calibration function
### for all pollutants in our dataset

import datetime as dt
import numpy as np
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report, classification
from sklearn.ensemble import RandomForestClassifier

### read in the data and format some columns
### IMPORTANT NOTE:
### this is for reading in a specific csv file;
### name may need to be changed and location may be specified
### if used in different context
data = pd.read_csv('warning_level_data.csv', header = 0)
data['StartDate'] = pd.to_datetime(data.StartDate)
data.WarningCode = data.WarningCode.astype(int)

#### convert date to a time delta from today in days
data['TimeDelta']=(data.StartDate.apply(lambda x: (dt.datetime.today()-x).days))

### get the list of pollutants in our dataset
pollutants = data.Pollutant.unique()

### import the calibration function for them
import calibration_function

### use the calibration function on the dataset
def parameters_calibrated(data, pollutants):
    pollutant_models = {}
    for i in range(len(pol)):
        pollutant_models[pol[i]] = best_params(data, i)
    return pollutant_models
