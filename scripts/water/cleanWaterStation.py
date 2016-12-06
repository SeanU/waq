#!/usr/bin/env python

import csv
import pandas as pd
import sys

from os import path

from common import set_suffix, get_county_map, get_state_code, id_to_state

def clean_water_station(input_path):
    output_path = set_suffix(input_path, 'clean')
    state_code = get_state_code(input_path)

    print("Reading from {}. . .".format(input_path))
    data = pd.read_csv(input_path,
                    dtype={"HUCEightDigitCode": object, "StateCode" :object, "CountyCode" : object},
                    low_memory=False)
    print("Read {0} rows".format(len(data)))

    # Some stations have an incorrect sign on the longitude
    print("Inverting positive longitudes. . .")
    data.ix[data.LongitudeMeasure > 0, "Edits"] = "Inverted Longitude"
    data.ix[data.LongitudeMeasure > 0, "LongitudeMeasure"] *= -1
#   print("{0} locations teleported from China."
#         .format(len(data.ix[data.Edits == "Inverted Longitude"])))

    data["State"] = data.StateCode.map(id_to_state)
    county = get_county_map(state_code)
    data["CountyName"] = data.CountyCode.map(county)

    noCounty = data.ix[pd.isnull(data.CountyName)]
    print("{} stations have no county".format(len(noCounty)))

    data = data[['OrganizationFormalName',
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
                    'StateCode',
                    'State',
                    'CountyCode',
                    'CountyName',
                    'AquiferName',
                    'FormationTypeText',
                    'AquiferTypeName',
                    'ProviderName',
                    'Edits']]

    data.columns = ['Organization',
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
                        'State',
                        'CountyCode',
                        'CountyName',
                        'AquiferName',
                        'FormationType',
                        'AquiferType',
                        'Provider',
                        'Edits']

    print("Saving data to {}. . .".format(output_path))
    data.to_csv(output_path, index=False, quoting = csv.QUOTE_ALL)
    return output_path

if(__name__ == '__main__'):
    if len(sys.argv) < 2:
        print('Usage: cleanWaterStation.py [root-dir]')
        exit(-1)
    else:
        print(clean_water_station(sys.argv[1]))
