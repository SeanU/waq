#! /usr/bin/env python

import datetime as dt
import requests

from os import path, listdir
from dateutil.parser import parse as parsedate

#dictionary of FIPS state codes for US states and territories
state_codes = {'AL': '01', 'AK': '02', 'AS': '60', 'AZ': '04', 'AR': '05', 'CA': '06',
               'CO': '08', 'CT': '09', 'DE': '10', 'DC': '11', 'FL': '12', 'FM': '64',
               'GA': '13', 'GU': '66', 'HI': '15', 'ID': '16', 'IL': '17', 'IN': '18',
               'IA': '19', 'KS': '20', 'KY': '21', 'LA': '22', 'ME': '23', 'MH': '68',
               'MD': '24', 'MA': '25', 'MI': '26', 'MN': '27', 'MS': '28', 'MO': '29',
               'MT': '30', 'NE': '31', 'NV': '32', 'NH': '33', 'NJ': '34', 'NM': '35',
               'NY': '36', 'NC': '37', 'ND': '38', 'MP': '69', 'OH': '39', 'OK': '40',
               'OR': '41', 'PW': '70', 'PA': '42', 'PR': '72', 'RI': '44', 'SC': '45',
               'SD': '46', 'TN': '47', 'TX': '48', 'UM': '74', 'UT': '49', 'VT': '50',
               'VA': '51', 'VI': '78', 'WA': '53', 'WV': '54', 'WI': '55', 'WY': '56'}

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

def getFileEndDate(file):
    name, _ = path.splitext(file)
    enddate = str.split(name, sep='_')[-1]
    return parsedate(enddate)

def getLatestFileDate(dir):
    dates = [getFileEndDate(f)
             for f in listdir(dir)
             if path.isfile(path.join(dir, f))]
    if len(dates) > 0:
        return max(dates)
    else:
        return parsedate('01-01-2010')

def formatDate(date, sortable=False):
    if(sortable):
        return dt.date.strftime(date, '%Y%m%d')
    else:
        return dt.date.strftime(date, '%m-%d-%Y')

