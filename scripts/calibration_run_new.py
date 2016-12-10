### this code runs the calibration function
### for all pollutants in our dataset

import datetime as dt
import numpy as np
import pandas as pd

import math

from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report, classification
from sklearn.ensemble import RandomForestClassifier

### read in the data and format some columns
### IMPORTANT NOTE:
### this is for reading in a specific csv file;
### name may need to be changed and location may be specified
### if used in different context
# data = pd.read_csv('warning_level_data.csv', header = 0)

### read in the measurements and their stations
pollution_values = pd.read_csv("processed/all-result.csv", low_memory=False)
pollution_stations = pd.read_csv("processed/all-station.csv", low_memory=False)

pollution_stations['LocationIdentifier']= pollution_stations['MonitoringLocationId']

### select only anorganic data
dis_byproducts = pollution_values[pollution_values.Category =='Disinfection Byproducts']
print dis_byproducts.size
inorganic = pollution_values[pollution_values.Category =='Inorganic']
print inorganic.size
chemical_data = pd.concat([dis_byproducts, inorganic])
print chemical_data.size

### assign it to station
full_data = pd.merge(chemical_data, pollution_stations, on='LocationIdentifier', how='outer')

print full_data.size

##### THIS NEEDS TO BE CHANGED LATER - it if for running things locally and only for California
full_data = full_data[full_data.State == 'CA']


### drop unnecessary columns:
data = full_data.drop('Category', 1)
data = data.drop(['Unnamed: 0_x', 'ExceedsMcl', 'ExceedsMclg'], axis=1)
data = data.drop(['Mcl', 'Mclg', 'Rank', 'Unit', 'Unnamed: 0.1', 'VerticalMeasureUnit', 'StateCode'], axis=1)
data = data.drop(['Medium', 'Unnamed: 0_y', 'Organization', 'MonitoringLocationId', 'MonitoringLocationName', 'VerticalMeasure'], axis = 1)
data = data.drop(['MonitoringLocationType', 'MonitoringLocationDescription', 'HUC', 'DrainageArea'], 1)
data = data.drop(['State', 'CountyCode','CountyName','AquiferName','FormationType','AquiferType','Provider','Edits'], 1)
data = data.drop(['DrainageAreaUnit','ContributingDrainageArea','ContributingDrainageAreaUnit'], 1)

#drop measurements where concentration value is an invalid number

data = data[data.Value >= 0]

print data.size

#data = dataset

print data.head()
    
### convert the warning level into a numeric value
def level_convert(level):
    if (level == 'green'):
        return 0
    if (level == 'amber'):
        return 1    
    if (level =='red'):
        return 2
    else:
        return "N/A"
data["WarningCode"] = map(level_convert, data.WarningLevel )

### drop the rows with pollution level N/A
#data = data[data.WarningCode !='N/A']

### here, 'data' was uploaded in the main file
#data['Date'] = pd.to_datetime(data['StartDate'])
#dfmi.loc[:,('one','second')]

data = data[data.StartDate != '5005-05-23']

data.loc[:,'Date']= pd.to_datetime(data.loc[:, 'StartDate'])
data.loc[:, 'WarningCode'] = (data.loc[:, 'WarningCode']).astype(int)

#data = data[data.Date != '5005-05-23']

#### convert date to a time delta from today in days
data.loc[:,'TimeDelta']=(data.Date.apply(lambda x: (dt.datetime.today()-x).days))
#data.loc[:,'TimeDelta'] = data.loc[:,'TimeDelta'].astype(float)

### make sure the values make sense:
print ('Warning Levels: ', data.WarningLevel.unique() )
print ('Warning Code: ', data.WarningCode.unique() )

### check if the timedeltas are unique too
td = data.TimeDelta.unique().astype(float)
print ('TimeDelta: ', data.TimeDelta.unique() )

no_nan = True
for t in td:
    if (math.isnan(t) == True):
        no_nan = False
        print ('There is a NaN among the time deltas')

#no_nan = True
#for t in td:
    #if (math.isnan(t) == True):
        #no_nan = False
        #print ('There is a NaN among the time deltas')
if (no_nan == True):
    print ('There is no Nan among the time deltas')
    
### check the Latitude and Longitude parameters as well

print ('Latitude: ', data.Latitude.unique() )
print ('Longitude: ', data.Longitude.unique() )

        
        
### get the list of pollutants in our dataset
polls = data.Pollutant.unique()

print polls
print len(polls)

### import the calibration function for them
import calibration_function_new

### use the calibration function on the dataset
def parameters_calibrated(data, polls):
    pollutant_models = {}
    for i in range(len(polls)):
        pollutant_models[polls[i]] = calibration_function_new.best_params(data, polls[i])
    return pollutant_models

print parameters_calibrated(data, polls)