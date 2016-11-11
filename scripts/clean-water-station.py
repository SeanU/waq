#!/usr/bin/env python

import csv
import pandas as pd

from os import path


rootdir = '../data/water'

input_file = 'CA-station.csv'
county_file = 'CA-county-codes.csv'

input_base = path.splitext(input_file)[0]

input_path = path.join(rootdir, input_file)
county_path = path.join(rootdir, county_file)
output_path = path.join(rootdir, input_base + "-clean.csv")


print("Reading from {}. . .".format(input_path))
data = pd.read_csv(input_path,
                   dtype={"HUCEightDigitCode": object},
                   low_memory=False)
print("Read {0} rows".format(len(data)))

# Some stations have an incorrect sign on the longitude
print("Inverting positive longitudes. . .")
data.ix[data.LongitudeMeasure > 0, "Edits"] = "Inverted Longitude"
data.ix[data.LongitudeMeasure > 0, "LongitudeMeasure"] *= -1
print("{0} locations teleported from China."
      .format(len(data.ix[data.Edits == "Inverted Longitude"])))

print("Reading counties from {}. . .".format(county_path))
county = pd.read_csv(county_path)

merged = pd.merge(data, county, on='CountyCode', how='left')

noCounty = merged.ix[pd.isnull(merged.CountyName)]
print("{} stations have no county".format(len(noCounty)))


merged = merged[['OrganizationFormalName',
                 'MonitoringLocationIdentifier',
                 'MonitoringLocationName',
                 'MonitoringLocationTypeName',
                 'MonitoringLocationDescriptionText',
                 'HUCEightDigitCode',
                 'DrainageAreaMeasure/MeasureValue',
                 'DrainageAreaMeasure/MeasureUnitCode',
                 'ContributingDrainageAreaMeasure/MeasureValue',
                 'ContributingDrainageAreaMeasure/MeasureUnitCode',
                 'LatitudeMeasure',
                 'LongitudeMeasure',
                 'VerticalMeasure/MeasureValue',
                 'VerticalMeasure/MeasureUnitCode',
                 'StateCode_x',
                 'CountyCode',
                 'CountyName',
                 'AquiferName',
                 'FormationTypeText',
                 'AquiferTypeName',
                 'ProviderName',
                 'Edits']]

merged.columns = ['Organization',
                  'MonitoringLocationId',
                  'MonitoringLocationName',
                  'MonitoringLocationType',
                  'MonitoringLocationDescription',
                  'HUC',
                  'DrainageArea',
                  'DrainageAreaUnit',
                  'ContributingDrainageArea',
                  'ContributingDrainageAreaUnit',
                  'Latitude',
                  'Longitude',
                  'VerticalMeasure',
                  'VerticalMeasureUnit',
                  'StateCode',
                  'CountyCode',
                  'CountyName',
                  'AquiferName',
                  'FormationType',
                  'AquiferType',
                  'Provider',
                  'Edits']

print("Saving data to {}. . .".format(output_path))
merged.to_csv(output_path, index=False, quoting = csv.QUOTE_ALL)
