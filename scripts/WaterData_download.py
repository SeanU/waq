import requests
import re
import datetime as dt
import dateutil.parser as du

#function to download a file stream
def downloadFile(url):
    local_filename = re.sub(r'\W', '', url.split('/')[-1]) + '.zip'
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

#generates the URL to pull data from the Water Quality Portal
def generateUrl(state='CA', startDate=None, endDate=None):
    """
    generates a URL from the inputs for th WQP service
    
    ::state::  [string] a two-character FIPS US state code
    ::startDate::  [string|none] beginning date of the query, `None` uses yesterday's date
    ::endDate::  [string|none] end date of the query, `None` uses today's date
    
    note: ambiguous day and month combinations will defaul to the US standard of
          month/day/year. 
    """
    #dictionary of FIPS state codes for US states and territories
    state_codes = {'AL': '01', 'AK': '02', 'AS': '60', 'AZ': '04', 'AR': '05', 'CA': '06', 
                   'CO': '08', 'CT': '09', 'DE': '10', 'DC': '11', 'FL': '12', 'FM': '64', 
                   'GA': '13', 'GU': '66', 'HI': '15', 'ID': '16', 'IL': '17', 'IN': '18', 
                   'IA': '19', 'KS': '20', 'KY': '21', 'LA': '22', 'ME': '23', 'MH': '68', 
                   'MD': '24', 'MA': '25', 'MI': '26', 'MN': '27', 'MS': '28', 'MO': '29', 
                   'MT': '30', 'NE': '31', 'NV': '32', 'NH': '33', 'NJ': '34', 'NM': '35', 
                   'NY': '36', 'NC': '37', 'ND': '38', 'MP': '69', 'OH': '39', 'OK': '40', 
                   'OR': '41', 'PW': '70', 'PA': '42', 'PR': '72', 'RI': '44', 'SC': '45', 
                   'SD': '46', 'TN': '47', 'TX': '48', 'UM': '74', 'UT': '49', 'VT': '50', 
                   'VA': '51', 'VI': '78', 'WA': '53', 'WV': '54', 'WI': '55', 'WY': '56'}
    
    #check for the proper state input
    assert isinstance(state, str), '`state` must be a two letter string in the FIPS state codes'
        
    #states are referred to by a number based on the above dictionary
    #translate state abrievation input into the correct number
    stateNo = state_codes[state.upper()]
    
    #convert startdate into correct format
    if startDate:
        start = dt.date.strftime(du.parse(startDate), '%m-%d-%Y')
    else:
        start = dt.date.strftime(dt.date.today() + dt.timedelta(-1), '%m-%d-%Y')
    
    if endDate:
        end = dt.date.strftime(du.parse(endDate), '%m-%d-%Y')
    else:
        end = dt.date.strftime(dt.date.today(), '%m-%d-%Y')
    
    
    url = ('http://www.waterqualitydata.us/Result/search?'
           +'countrycode=US'+'&statecode=' + stateNo
           +'&startDataLo=' + start
           +'&startDateHi=' + end
           +'&mimeType=tsv&zip=yes&sorted=no')
    
    return url


#to download all of the data, use an early startDate and leave endDate as None
#to just download the last days data leave both startDate and endDate as None
#downloadFile(generateUrl('CA', startDate='01-01-1980'))


#download all of the historic data for each state
states = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'FM', 
    'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 
    'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 
    'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 
    'SD', 'TN', 'TX', 'UM', 'UT', 'VT', 'VA', 'VI', 'WA', 'WV', 'WI', 'WY']

for state in states:
    downloadFile(generateUrl(state, startDate='01-01-1970'))


#pull the updated (last 24 hours) of data for all US
for state in states:
    downloadFile(generateUrl(state))