#!/usr/bin/env python

import csv
import pandas as pd
import re
import sys

from os import path
from common import set_suffix

if len(sys.argv) < 2:
      print('Usage: clean-water-station.py [root-dir]')
      exit(-1)

input_path = sys.argv[1]
output_path = set_suffix(input_path, 'clean')

measure_to_measure_group = 'measure-to-measuregroup.csv'

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
    'ResultCommentText',
    'OrganizationIdentifier',
    'OrganizationFormalName',
    'ActivityTypeCode',
    'ResultSampleFractionText',
    'MeasureQualifierCode',
    'ResultStatusIdentifier',
    'ResultAnalyticalMethod/MethodIdentifier',
    'ResultAnalyticalMethod/MethodName',
    'ResultLaboratoryCommentText'
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

measures = pd.read_csv(measure_to_measure_group)


data = pd.read_csv(input_path,
                   error_bad_lines=False,
                   usecols=data_columns)

print("loaded {0} rows".format(len(data)))

data["Value"] = pd.to_numeric(data.ResultMeasureValue, errors='coerce')

print("Removing non-water data. . .")
data = data[data.ActivityMediaName.isin(activity_media)]
print("{0} rows remain".format(len(data)))

print("Removing unparseable values. . .")

data = data[pd.notnull(data.Value)]
print("{0} rows remain".format(len(data)))


print("Assigning measure data. . .")
measureMap = pd.DataFrame(data.CharacteristicName.unique(),
                          columns=['CharacteristicName'])

for _, row in measures.iterrows():
    pattern = re.compile(row.Pattern, re.IGNORECASE)
    matches = measureMap.CharacteristicName.str.contains(row.Pattern,
                                                         case=False)
    measureMap.loc[matches, 'MeasureGroup'] = row.MeasureGroup
    measureMap.loc[matches, 'MCLG'] = row.MCLG
    measureMap.loc[matches, 'Unit'] = row.Unit

measureMap = measureMap[pd.notnull(measureMap.MeasureGroup)]
data = pd.merge(data, measureMap, on='CharacteristicName')


print("Finding non-matched measures. . . ")

data = data[pd.notnull(data.MeasureGroup)]
print("{0} values remain".format(len(data)))

data['OriginalUnit'] = data['ResultMeasure/MeasureUnitCode'].str.strip()


print("Merging in multiplier data. . .")
merged = pd.merge(data, multipliers, on='OriginalUnit', how='left')


print("Finding unrecognized units...")
unmappedUnits = merged.loc[pd.isnull(merged.Multiplier)]

merged = merged.loc[pd.notnull(merged.Multiplier)]
merged['OriginalValue'] = merged.Value
merged.Value = merged.Value * merged.Multiplier
print("{0} rows remain".format(len(merged)))


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
                  'ResultCommentText',
                  'OrganizationIdentifier',
                  'OrganizationFormalName',
                  'ActivityTypeCode',
                  'ResultSampleFractionText',
                  'MeasureQualifierCode',
                  'ResultStatusIdentifier',
                  'ResultAnalyticalMethod/MethodIdentifier',
                  'ResultAnalyticalMethod/MethodName',
                  'ResultLaboratoryCommentText'
                  ]]

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
                   'Comment',
                   'OrganizationId',
                   'OrganizationName',
                   'ActivityTypeCode',
                   'ResultSampleFraction',
                   'QualifierCode',
                   'ResultStatus',
                   'AnalyticalMethodIdentifier',
                   'AnalyticalMethodName',
                   'LaboratoryComment'
                   ]

print("Saving output")
keepers.to_csv(output_path, index=False, quoting=csv.QUOTE_ALL)
