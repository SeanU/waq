import csv
import re
import pandas as pd
import sys
from common import set_suffix

def clean_water_bio(input_path):
    output_path = set_suffix(input_path, 'biological')

    # list of CharacteristicName values we are interested in
    bio_names =  ['Fecal Coliform', 'Enterococcus', 'Escherichia coli', 'Total Coliform']

    # list of columns we will need
    cols = ['MonitoringLocationIdentifier', 'CharacteristicName',
            'ActivityStartDate', 'ActivityStartTime/Time',
            'ResultMeasureValue', 'ResultMeasure/MeasureUnitCode']

    print("loading " + input_path)
    # open the file for reading, pass it to the CSV dict reader
    # this will return each row as a dictionary where the keys 
    # are the header row
    with open(input_path, 'r') as fp:
        reader = csv.DictReader(fp)
        # iterate over each row, form a sublist of just the columns
        # we are interested in, only if the CharacteristicName is in
        # the bio_names list
        data = [[row[c] for c in cols] for row in reader 
                    if ('mpn' in row['ResultMeasure/MeasureUnitCode'].lower() or 
                        'cfu' in row['ResultMeasure/MeasureUnitCode'].lower())]
                    
    # pass the data to a dataframe along with the columns
    df = pd.DataFrame(data, columns=cols)

    #map poor spellings to bio_names standards
    def name_cleaner(name_string):
        if re.match('fecal', name_string, re.IGNORECASE):
            return "Fecal Coliform"
        if re.match('total col', name_string, re.IGNORECASE):
            return "Total Coliform"
        if re.match('enteroc', name_string, re.IGNORECASE):
            return "Enterococcus"
        if re.match('escherich|e\.coli|e\. coli', name_string, re.IGNORECASE):
            return "Escherichia coli"
        #we drop anything else because there are very few other biologicals measured
        #and they vary widely
        return 'DROP'
    
    #apply the name cleaner fumction to the data and drop any other columns        
    df.CharacteristicName = df.CharacteristicName.apply(name_cleaner)
    df.drop(df[df.CharacteristicName == 'DROP'].index, inplace = True)


    # define a function to create the Status columns
    def set_status(val_string):
        try:
            # try to convert to float
            val = float(re.sub(r'[<>,]', '', val_string))
        except:
            # handle all of the cases in which that fails
            if re.match(r'absen|nd|not detected', val_string, re.IGNORECASE):
                return 'green'
            elif re.match(r'\d+\-\d+', val_string):
                val = float(re.findall(r'(\d+)\-\d+', val_string)[0])
            elif re.match(r'present above quantification limit', val_string, re.IGNORECASE):
                return 'red'
            else:
                # catch all case
                return 'nan'
        # use the float value to convert to a status
        if 0.0 <= val <= 1.0:
            return 'green'
        elif 1.0 < val <= 10.0:
            return 'amber'
        elif val > 10.0:
            return 'red'

    # create blank dataframe for output formatting
    df_out = pd.DataFrame()
    df_out['LocationIdentifier'] = df['MonitoringLocationIdentifier']
    df_out['Medium'] = 'Water'
    df_out['StartDate'] = df['ActivityStartDate']
    df_out['StartTime'] = df['ActivityStartTime/Time']
    df_out['Category'] = 'biological'
    df_out['Pollutant'] = df['CharacteristicName']
    df_out['Unit'] = 'CFU'
    df_out['Mclg'] = 0
    df_out['Mcl'] = 10
    df_out['Value'] = df['ResultMeasureValue']
    df_out['WarningLevel'] = df.ResultMeasureValue.apply(set_status)
    # drop the 'nan' Status values from the dataframe
    df_out.drop(df_out.index[df_out.WarningLevel=='nan'], inplace=True)
    # also drop the duplicate measurements.  this is where a breakdown
    # of a sub-measurement is in a column we already dropped.
    df_out = df_out.drop_duplicates()
    df_out = df_out[pd.notnull(df_out.WarningLevel)]
    df_out.reset_index(inplace=True, drop=True)
    # push to file
    print("Saving " + output_path)
    df_out.to_csv(output_path, index = False)
    return output_path

if(__name__ == '__main__'):
    if len(sys.argv) < 2:
        print('Usage: cleanWaterBio.py [root-dir]')
        exit(-1)
    else:
        print(clean_water_bio(sys.argv[1]))
