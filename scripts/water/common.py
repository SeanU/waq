#! /usr/bin/env python

import requests

from os import path, listdir
import pandas as pd
import datetime as dt

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

# Generating dictionaries for mapping FIPS codes
fips = pd.read_csv('fips_codes.csv', dtype={'StateCode': object, 'CountyCode': object})
state_index = fips[['State', 'StateCode']].drop_duplicates()
state_to_id = state_index.set_index('State').to_dict()['StateCode']
id_to_state = state_index.set_index('StateCode').to_dict()['State']
del state_index

def get_county_map(state):
    map =  fips.ix[fips.State == state][['CountyCode', 'CountyName']]\
        .set_index('CountyCode')\
        .to_dict()['CountyName']
    return map

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
