#!/usr/bin/env python

import datetime as dt
import sys

from os import path

from common import state_codes, downloadFile, getLatestFileDate, formatDate


def generateUrl(state, startDate, endDate):
    """
    generates a URL from the inputs for th WQP service
    
    ::state::  [string] a two-character FIPS US state code
    ::startDate::  [string|none] beginning date of the query, `None` uses yesterday's date
    ::endDate::  [string|none] end date of the query, `None` uses today's date
    
    note: ambiguous day and month combinations will defaul to the US standard of
          month/day/year. 
    """
    
    #check for the proper state input
    assert isinstance(state, str), '`state` must be a two letter string in the FIPS state codes'
    
    #states are referred to by a number based on the above dictionary
    #translate state abrievation input into the correct number
    stateNo = state_codes[state.upper()]
    
    #convert startdate into correct format
    start = formatDate(startDate)
    end = formatDate(endDate)
    
    url = ('http://www.waterqualitydata.us/Station/search?'
           +'countrycode=US'+'&statecode=US%3A' + stateNo
           +'&startDataLo=' + start
           +'&startDateHi=' + end
           +'&mimeType=csv&zip=yes&sorted=no')
    
    return url

def generateFilePath(root, state, startDate, endDate):
    filename = "{}_{}_{}.zip".format(state, 
                                    formatDate(startDate, sortable=True), 
                                    formatDate(endDate, sortable=True))
    return path.join(root, filename)

def downloadWaterStationData(root, state, startDate, endDate):
    url = generateUrl(state, startDate, endDate)
    path = generateFilePath(root, state, startDate, endDate)
    return downloadFile(url, path)

def main(root):
    yesterday = dt.datetime.today() - dt.timedelta(days=1)
    for state in state_codes:
        subdir = path.join(root, state, 'water', 'station')
        latestDate = getLatestFileDate(subdir)
        if latestDate < yesterday :
            startDate = latestDate  + dt.timedelta(days=1)
            print("Getting {} station data between {} and {}"\
                    .format(state, formatDate(startDate), formatDate(yesterday)))
            downloadWaterStationData(subdir, state, latestDate, yesterday)
        else:
            print("{} station data is up to date".format(state))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: download-water-station.py [root-dir]')
    else:
        main(sys.argv[1])
