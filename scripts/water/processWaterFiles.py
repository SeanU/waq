#!/usr/bin/env python

import sys
import zipfile
import re
import pandas as pd

from os import path, remove, rename, walk

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
    renamed = path.join(root, state + '_station.csv')
    rename(unzipped, renamed)
    cleaned = clean_water_station(renamed)
    remove(renamed)


def clean_result_data(root, state):
    zippath = generateFilePath(root, state, 'result')
    unzip(zippath)
    unzipped = path.join(root, 'result.csv')
    renamed = path.join(root, state + '_result.csv')
    rename(unzipped, renamed)
    cleaned = clean_water_result(renamed)
    aggregated = aggregate_water_result(cleaned)
    bio = clean_water_bio(renamed)
    remove(renamed)
    remove(cleaned)

def merge_data(root):
    def enumerate_files(folder, pattern):
        for dirpath, dirnames, filenames in walk(folder):
            for f in filenames:
                if re.match(pattern, f):
                    print('Enumerating ' + f)
                    yield path.join(dirpath, f)

    def read_and_rank(path):
        df = pd.read_csv(path, low_memory=False)
        df['Date'] = df['StartDate'] + ' ' + df['StartTime']
        df['Rank'] = df.sort_values('Date')\
                        .groupby(['LocationIdentifier', 'Pollutant'])\
                        .cumcount() + 1
        return df.drop('Date', 1)

    def merge_station_files(folder):
        dfs = [pd.read_csv(f, low_memory=False) 
            for f in enumerate_files(folder, r'\w\w_station-.*\.csv')]
        return pd.concat(dfs)

    def merge_rank_result_files(folder):
        dfs = [read_and_rank(f) 
            for f in enumerate_files(folder, r'\w\w_result-.*\.csv')]
        return pd.concat(dfs)

    print("Concatenating stations")
    merge_station_files(root)\
        .to_csv(path.join(root, path.join(root, 'all-station.csv')))

    print("Concatenating results")
    merge_rank_result_files(root)\
        .to_csv(path.join(root, path.join('all-result.csv')))

def main(root):
    for state in sorted(state_to_id):
        subdir = path.join(root, state)
        if path.exists(subdir):
            clean_station_data(subdir, state)
            clean_result_data(subdir, state)
    merge_data(root)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: download-water-station.py [root-dir]')
    else:
        main(sys.argv[1])
