#! /usr/bin/env python

import requests

from os import path, listdir
import pandas as pd
import datetime as dt


# Generating dictionaries for mapping FIPS codes
fips = pd.read_csv('fips_codes.csv', dtype={'StateCode': object, 'CountyCode': object})
state_index = fips[['State', 'StateCode']].drop_duplicates()
state_to_id = state_index.set_index('State').to_dict()['StateCode']
id_to_state = state_index.set_index('StateCode').to_dict()['State']
del state_index

def get_county_map(state):
    return fips.ix[fips.State == state]

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

def set_suffix(filepath, suf):
    folder, file = path.split(filepath)
    name, ext = path.splitext(file)
    name = name.split('-')[0]
    return path.join(folder, name + '-' + suf + ext)

def get_state_code(filepath):
    _, file = path.split(filepath)
    return file[:2]
