#!/usr/bin/env python

import csv
import pandas as pd

resultpath = '../data/water/CA-result-clean.csv'
measuregrouppath = '../data/water/measuregroup.csv'
outputpath = '../data/water/CA-result-withmeasuregroup.csv'

data = pd.read_csv(resultpath)
mcls = pd.read_csv(measuregrouppath,
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

withmcls = withmcls[['LocationIdentifier',
                     'Medium',
                     'MediumSubdivision',
                     'StartDate',
                     'StartTime',
                     'TimeZone',
                     'Category',
                     'Pollutant',
                     'Unit',
                     'Mclg',
                     'Mcl',
                     'Value',
                     'ExceedsMclg',
                     'ExceedsMcl',
                     'Comment']]

withmcls.ix[withmcls.ExceedsMclg == 0, 'WarningLevel'] = 'Green'
withmcls.ix[(withmcls.ExceedsMclg > 0) & (withmcls.ExceedsMcl is False),
            'WarningLevel'] = 'Amber'
withmcls.ix[withmcls.ExceedsMcl, 'WarningLevel'] = 'Red'

# Output
withmcls.to_csv(outputpath, quoting=csv.QUOTE_ALL, index=False)
print(outputpath)
