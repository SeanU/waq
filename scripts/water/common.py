#! /usr/bin/env python

import requests

from os import path, listdir
import pandas as pd
import datetime as dt


# Generating dictionaries for mapping FIPS codes
fips = pd.read_csv('fips_codes.csv', dtype={'StateId': object, 'CountyId': object})
state_index = fips[['State', 'StateId']].drop_duplicates()
state_to_id = state_index.set_index('State').to_dict()['StateId']
id_to_state = state_index.set_index('StateId').to_dict()['State']
del state_index

def get_county_data(state):
    county = fips.ix[fips.State == state]
    return county[['County', 'CountyId']].drop_duplicates()

def get_county_to_id(state):
    county_index = get_county_data(state)
    return county_index.set_index('County').to_dict()['CountyId']

def get_id_to_county(state):
    county_index = get_county_data(state)
    return county_index.set_index('CountyId').to_dict()['County']

water_file_types = ['station', 'result']

def downloadFile(url, path):
    print('{}\t Downloading {}'.format(dt.datetime.now(), path))
    # NOTE the stream=True parameter
    request = requests.get(url, stream=True)
    with open(path, 'wb') as file:
        for chunk in request.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                file.write(chunk)


    print('{}\t Finished downloading {}'.format(dt.datetime.now(), path))
    return path
