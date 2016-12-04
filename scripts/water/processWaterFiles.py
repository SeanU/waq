#!/usr/bin/env python

import sys
import zipfile

from os import path, remove

from common import state_to_id, downloadFile
from cleanWaterStation import clean_water_station
from cleanWaterResult import clean_water_result
from aggregateWaterResult import aggregate_water_result
from cleanWaterBio import clean_water_bio

def generateFilePath(root, state, kind):
    filename = "{}_{}.zip".format(state, kind)
    return path.join(root, filename)

def unzip(filepath):
    name, _ = path.splitext(filepath)
    outfolder, _ = path.split(filepath)
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(outfolder)

def clean_station_data(root, state):
    zippath = generateFilePath(root, state, 'station')
    unzip(zippath)
    unzipped = path.join(root, 'station.csv')
    cleaned = clean_water_station(unzipped)
    remove(unzipped)


def clean_result_data(root, state):
    zippath = generateFilePath(root, state, 'result')
    unzip(zippath)
    unzipped = path.join(root, 'result.csv')
    cleaned = clean_water_result(unzipped)
    aggregated = aggregate_water_result(cleaned)
    bio = clean_water_bio(unzipped)
    remove(unzipped)
    remove(cleaned)

def main(root):
    for state in state_to_id:
        subdir = path.join(root, state)
        if path.exists(subdir):
            clean_station_data(subdir, state)
            clean_result_data(subdir, state)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: download-water-station.py [root-dir]')
    else:
        main(sys.argv[1])
