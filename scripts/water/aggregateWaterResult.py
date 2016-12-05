#!/usr/bin/env python

import csv
import sys
import pandas as pd

from common import set_suffix

def aggregate_water_result(input_path):
    output_path = set_suffix(input_path, 'chemical')

    print("loading " + input_path)
    data = pd.read_csv(input_path,
                    low_memory=False)
    mcls = pd.read_csv('measuregroup.csv',
                    usecols=['MeasureGroup', 'Category', 'MCL'])
    mcls.columns = ['Pollutant', 'Category', 'Mcl']


    # Aggregating PCBs
    pcbdata = data.ix[data.PollutantGroup == 'PCBs']\
        .sort_values(['LocationIdentifier', 'StartDate', 'Pollutant'])
    pcbsums = pcbdata.groupby(['LocationIdentifier', 'StartDate'])\
                    .sum()
    pcbgroups = pcbdata.groupby(['LocationIdentifier', 'StartDate'])\
                    .first()
    pcbgroups = pcbgroups.drop(['Value', 'Mclg', 'ExceedsMclg'], axis=1)
    pcbs = pcbgroups.join(pcbsums).reset_index()
    pcbs.Pollutant = 'PCBs'

    # Aggregating HAA5
    haa5data = data.ix[data.PollutantGroup == 'HAA5']\
        .sort_values(['LocationIdentifier', 'StartDate', 'Pollutant'])
    haa5sums = haa5data.groupby(['LocationIdentifier', 'StartDate'])\
                    .sum()
    haa5groups = haa5data.groupby(['LocationIdentifier', 'StartDate'])\
                        .first()
    haa5groups = haa5groups.drop(['Value', 'Mclg', 'ExceedsMclg'], axis=1)
    haa5 = haa5groups.join(haa5sums).reset_index()
    haa5.Pollutant = 'HAA5'

    # Aggregating TTHMs
    tthmdata = data.ix[data.PollutantGroup == 'TTHMs']\
        .sort_values(['LocationIdentifier', 'StartDate', 'Pollutant'])
    tthmsums = tthmdata.groupby(['LocationIdentifier', 'StartDate'])\
                    .sum()
    tthmgroups = tthmdata.groupby(['LocationIdentifier', 'StartDate'])\
                        .first()
    tthmgroups = tthmgroups.drop(['Value', 'Mclg', 'ExceedsMclg'], axis=1)
    tthms = tthmgroups.join(tthmsums).reset_index()
    tthms.Pollutant = 'TTHMs'

    # Aggregating Xylenes
    xylenedata = data.ix[data.PollutantGroup == 'Xylene']\
        .sort_values(['LocationIdentifier', 'StartDate', 'Pollutant'])
    xylenesums = xylenedata.groupby(['LocationIdentifier', 'StartDate'])\
                        .sum()
    xylenegroups = xylenedata.groupby(['LocationIdentifier', 'StartDate'])\
                            .first()
    xylenegroups = xylenegroups.drop(['Value', 'Mclg', 'ExceedsMclg'], axis=1)
    xylene = xylenegroups.join(xylenesums).reset_index()
    xylene.Pollutant = 'Xylene'

    # Re-joining
    nonaggs = data.ix[
        ~data.PollutantGroup.isin(['PCBs', 'HAA5', 'TTHMs', 'Xylene'])]
    rejoined = pd.concat([nonaggs, pcbs, haa5, tthms, xylene])\
                .drop('PollutantGroup', axis=1)

    # Applying MCLs
    withmcls = pd.merge(rejoined, mcls, on="Pollutant")
    withmcls['ExceedsMcl'] = withmcls.Value > withmcls.Mcl

    withmcls.ix[withmcls.ExceedsMclg == 0, 'WarningLevel'] = 'green'
    withmcls.ix[(withmcls.ExceedsMclg > 0) & (withmcls.ExceedsMcl is False),
                'WarningLevel'] = 'amber'
    withmcls.ix[withmcls.ExceedsMcl, 'WarningLevel'] = 'red'

# Restricting column list for compatiblity with bio data
    withmcls = withmcls[[
        'LocationIdentifier',
        'Medium',
        # 'MediumSubdivision',  # Unused
        'StartDate',
        'StartTime',
        # 'TimeZone',  # Unused
        'Category',
        'Pollutant',
        'Unit',
        'Mclg',
        'Mcl',
        'Value',
        'WarningLevel'
        # 'ExceedsMclg', # Unused
        # 'ExceedsMcl',  # Unused
        # 'Comment'     # Unused
        ]]


    # Output
    print("Saving " + output_path)
    withmcls.to_csv(output_path, quoting=csv.QUOTE_ALL, index=False)
    return output_path

if(__name__ == '__main__'):
    if len(sys.argv) < 2:
        print('Usage: aggregateWaterResult.py [root-dir]')
        exit(-1)
    else:
        print(aggregate_water_result(sys.argv[1]))
