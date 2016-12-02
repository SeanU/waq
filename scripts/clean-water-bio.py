import csv
import re
import pandas as pd

# list of CharacteristicName values we are interested in
bio_names =  ['Fecal Coliform', 'Enterococcus', 'Escherichia coli', 
              'Total Coliform']

# list of columns we will need
cols = ['MonitoringLocationIdentifier', 'CharacteristicName',
        'ActivityStartDate', 'ActivityStartTime/Time',
        'ResultMeasureValue']

# open the file for reading, pass it to the CSV dict reader
# this will return each row as a dictionary where the keys 
# are the header row
with open('G:/biologicalresult.csv', 'r') as fp:
    reader = csv.DictReader(fp)
    # iterate over each row, form a sublist of just the columns
    # we are interested in, only if the CharacteristicName is in
    # the bio_names list
    data = [row[c] for row in reader 
                   for c in cols
                   if (row['CharacteristicName'] in bio_names)]
                   
# pass the data to a dataframe along with the columns
df = pd.DataFrame(data, columns=cols)

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
        return 'yellow'
    elif val > 10.0:
        return 'red'

# read in the station data, reset the column names
station_cols = ['MonitoringLocationIdentifier', 'LatitudeMeasure', 'LongitudeMeasure']
station_cols_new = ['SiteID', 'Lat', 'Lng']
df_station = pd.read_csv('G:/station.csv', usecols=station_cols)
df_station.columns = station_cols_new
# oddly, the station data has duplicates.  so we drop the dupes
df_station = df_station.drop_duplicates(subset=['SiteID'])
df_station.reset_index(inplace=True, drop=True)

# create blank dataframe for output formatting
df_out = pd.DataFrame()
df_out['SiteID'] = df['MonitoringLocationIdentifier']
df_out['ContaminantType'] = 'Water'
df_out['Contaminant'] = df['CharacteristicName']
df_out['MeasurementDate'] = df['ActivityStartDate']
df_out['Code'] = ''
df_out['ContaminantCategory'] = 'biological'
# perform a left join with df_station.  this is why we
# renamed the df_station columns earlier
df_out = df_out.merge(df_station, on='SiteID', how='left')
df_out['MeasurementTime'] = df['ActivityStartTime/Time']
df_out['Rank'] = ''
df_out['solr_query'] = ''
# apply the color status to data
df_out['Status'] = df.ResultMeasureValue.apply(set_status)
df_out['Value'] = df['ResultMeasureValue']
# drop the 'nan' Status values from the dataframe
df_out.drop(df_out.index[df_out.Status=='nan'], inplace=True)
# also drop the duplicate measurements.  this is where a breakdown
# of a sub-measurement is in a column we already dropped.
df_out = df_out.drop_duplicates()
df_out.reset_index(inplace=True, drop=True)
# push to file
df_out.to_csv('G:/biological_cleaned.csv')



# use this section to write out the wanted lines to a new file
#with open('G:/biologicalresult.csv', 'rb') as fp1:
#    reader = csv.reader(fp1)
#    header = next(reader)
#    index = header.index('CharacteristicName')
#    with open('U:/biologicalresults_filtered.csv', 'wb') as fp2:
#        writer = csv.writer(fp2)
#        writer.writerow(header)
#        write_count = 0
#        for i, row in enumerate(reader):
#            if row[index] in bio_names:
#                writer.writerow(row)
#                write_count += 1
#            if i % 100000 == 0:
#                print('Rows read: %d, rows written: %d' %(i, write_count))