#!/usr/bin/env python

import datetime as dt
import sys

from os import path

from common import state_to_id, downloadFile

def generateUrl(state):
    #check for the proper state input
    assert isinstance(state, str), '`state` must be a two letter string in the FIPS state codes'
    
    #states are referred to by a number based on the above dictionary
    #translate state abrievation input into the correct number
    stateNo = state_to_id[state.upper()]
    
    url = ('http://www.waterqualitydata.us/Result/search?'
           +'countrycode=US'+'&statecode=US%3A' + stateNo
           +'&sampleMedia=Water&sampleMedia=water'
           +'&startDateLo=01-01-2010'
           +'&providers=NWIS&providers=STEWARDS&providers=STORET'
           +'&mimeType=csv&zip=yes&sorted=no')
    
    return url

def generateFilePath(root, state):
    filename = "{}_result.zip".format(state)
    return path.join(root, filename)

def downloadWaterResultData(root, state):
    url = generateUrl(state)
    path = generateFilePath(root, state)
    return downloadFile(url, path)

def main(root):
    for state in state_to_id:
        subdir = path.join(root, state)
        downloadWaterResultData(subdir, state)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: download-water-result.py [root-dir]')
    else:
        main(sys.argv[1])
