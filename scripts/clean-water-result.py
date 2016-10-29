#!/usr/bin/evn python

import csv
import pandas as pd
import re

from os import path

rootdir = '../data/water'

input_file = 'CA-result.csv'
measure_to_measure_group = 'measure-to-measuregroup.csv'

input_base = path.splitext(input_file)[0]

bad_values = 'badvalues.csv'
unmatched_measures = 'unmatched-measures.csv'
unmapped_units = 'unmapped-units.csv'
over1k = 'over-one-thousand.csv'
less_than_zero = 'less-than-zero.csv'
result_clean = 'clean.csv'


def makepath(suf):
    file = input_base + '-' + suf
    print(file)
    return path.join(rootdir, file)


data_columns = [
    'ActivityMediaName',
    'ActivityMediaSubdivisionName',
    'ActivityStartDate',
    'ActivityStartTime/Time',
    'ActivityStartTime/TimeZoneCode',
    'MonitoringLocationIdentifier',
    'CharacteristicName',
    'ResultMeasureValue',
    'ResultMeasure/MeasureUnitCode',
    'ResultCommentText'
]

activity_media = ['Water']

multipliers = pd.Series({
    'mg/l': 1,
    'mg/l as N': 1,
    'mg/kg': 1,
    'mg/kg as N': 1,
    'ug/l': 1 / 1000,
    'ug/kg': 1 / 1000,
    'ng/l': 1 / 1000000,
    'pg/l': 1 / 1000000000,
    'ppm': 1,
    'ppb': 1 / 1000,
    'ueq/l': 62
}, name='Multiplier')
multipliers.index.name = 'OriginalUnit'

multipliers = multipliers.reset_index()

measures = pd.read_csv(path.join(rootdir, measure_to_measure_group))


f = path.join(rootdir, input_file)
print("Loading {0}...".format(f))
data = pd.read_csv(f,
                   error_bad_lines=False,
                   usecols=data_columns)

print("loaded {0} rows".format(len(data)))

data["Value"] = pd.to_numeric(data.ResultMeasureValue, errors='coerce')

print("Removing non-water data. . .")
data = data[data.ActivityMediaName.isin(activity_media)]
print("{0} rows remain".format(len(data)))

print("Removing unparseable values. . .")
badValues = data.loc[pd.isnull(data.Value)]
badValues.to_csv(makepath(bad_values), index=False, quoting=csv.QUOTE_ALL)
print("{0} rows removed".format(len(badValues)))
del badValues

data = data[pd.notnull(data.Value)]
print("{0} rows remain".format(len(data)))


print("Assigning measure data. . .")
for _, row in measures.iterrows():
    print("\t" + row.Pattern)
    pattern = re.compile(row.Pattern, re.IGNORECASE)
    matches = data.CharacteristicName.str.contains(row.Pattern, case=False)
    data.loc[matches, 'MeasureGroup'] = row.MeasureGroup
    data.loc[matches, 'MCLG'] = row.MCLG
    data.loc[matches, 'Unit'] = row.Unit

print("Finding non-matched measures. . . ")
nonMatchingMeasures = \
    data.loc[pd.isnull(data.MeasureGroup), 'CharacteristicName'].unique()
pd.DataFrame(nonMatchingMeasures).to_csv(makepath(unmatched_measures),
                                         index=False, quoting=csv.QUOTE_ALL)
print("{0} rows didn't match".format(len(nonMatchingMeasures)))
del nonMatchingMeasures

data = data[pd.notnull(data.MeasureGroup)]
print("{0} values remain".format(len(data)))

data['OriginalUnit'] = data['ResultMeasure/MeasureUnitCode'].str.strip()


print("Merging in multiplier data. . .")
merged = pd.merge(data, multipliers, on='OriginalUnit', how='left')


print("Finding unrecognized units...")
unmappedUnits = merged.loc[pd.isnull(merged.Multiplier)]
unmappedUnits.to_csv(makepath(unmapped_units),
                     index=False,
                     quoting=csv.QUOTE_ALL)
print("{0} rows with unrecognized units".format(len(unmappedUnits)))
del unmappedUnits

merged = merged.loc[pd.notnull(merged.Multiplier)]
merged['OriginalValue'] = merged.Value
merged.Value = merged.Value * merged.Multiplier
print("{0} rows remain".format(len(merged)))


# Removing outliers - anything above 1g/L we'll assume is an outlier,
# though it may just be bad units and we can scale down by a factor of 1,000
print("Removing outliners - measurements over 1g/mL")
overOneThousand = merged.loc[merged.Value > 1000]
overOneThousand.to_csv(makepath(over1k), index=False, quoting=csv.QUOTE_ALL)
print("Found {0} outliers".format(len(overOneThousand)))
del overOneThousand

merged = merged.loc[merged.Value <= 1000]
print("{0} rows remain".format(len(merged)))


# Same for less than zero
print("Removing negative results...")
lessThanZero = merged.loc[merged.Value < 0]
lessThanZero.to_csv(makepath(less_than_zero),
                    index=False,
                    quoting=csv.QUOTE_ALL)
print("Found {0} negative vlaues".format(len(lessThanZero)))
del lessThanZero


merged = merged.loc[merged.Value >= 0]
print("{0} rows remain.".format(len(merged)))


merged['ExceedsMclg'] = merged.Value > merged.MCLG

keepers = merged[['ActivityMediaName',
                  'ActivityMediaSubdivisionName',
                  'ActivityStartDate',
                  'ActivityStartTime/Time',
                  'ActivityStartTime/TimeZoneCode',
                  'MonitoringLocationIdentifier',
                  'CharacteristicName',
                  'MeasureGroup',
                  'Unit',
                  'Value',
                  'MCLG',
                  'ExceedsMclg',
                  'ResultCommentText']]

keepers.columns = ['Medium',
                   'MediumSubdivision',
                   'StartDate',
                   'StartTime',
                   'TimeZone',
                   'LocationIdentifier',
                   'Pollutant',
                   'PollutantGroup',
                   'Unit',
                   'Value',
                   'Mclg',
                   'ExceedsMclg',
                   'Comment']

print("Saving output")
keepers.to_csv(makepath(result_clean), index=False, quoting=csv.QUOTE_ALL)
