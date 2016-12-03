#!/usr/bin/env python

import sys
import zipfile

from os import path, remove

from common import state_to_id, downloadFile
from cleanWaterStation import clean_water_station
from cleanWaterResult import clean_water_result
from aggregateWaterResult import aggregate_water_result

def generateFilePath(root, state, kind):
    filename = "{}-{}.zip".format(state, kind)
    return path.join(root, filename)

def unzip(filepath):
    name, _ = path.splitext(filepath)
    outfolder, _ = path.split(filepath)
    outpath = name + '.csv'
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(outfolder)
    return outpath

def clean_station_data(root, state):
    filepath = generateFilePath(root, state, 'station')
    unzipped = unzip(filepath)
    cleaned = clean_water_station(unzipped)
    remove(unzipped)
    return cleaned


def clean_result_data(root, state):
    filepath = generateFilePath(root, state, 'result')
    unzipped = unzip(filepath)
    cleaned = clean_water_result(unzipped)
    aggregated = aggregate_water_result(cleaned)
    remove(unzipped)
    remove(cleaned)
    return aggregated

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
