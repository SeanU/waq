import datetime as dt
import numpy as np
import pandas as pd
import re
import dill

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# to predict:
# unpickle the model
with open('trained_models.pickle', 'rb') as fp:
    meta_model = dill.load(fp, protocol=2)

# call predict function, returns list of lists of predictions
prediction_list = meta_model.estimated_pollution(lat, lng, time_delta=0)
