"""Use the ReadSnowData() function to download all records from API and compile into CSV's."""

# Load required modules and user defined functions
import os, urllib, re
import pandas as pd
from tqdm import tqdm
from ReadSnowData import ReadSnowData
from MultipleReplace import MultipleReplace

# Import meta data to pass to search queries
os.chdir('./snow-forecasting')
ntwk = pd.read_csv('snow-meta.csv')

# Define variable name abbreviations list where...
## T = temperature (average, maximum, minimum, observered), degrees F
## PREC = yearly accumulated precipitation at start of day, inches
## SNWD = snow depth at start of day, inches
## WTEQ = Depth of water that would theoretically result if the entire snowpack were melted instantaneously, inches
## STO:x = soil temperature observed at depth x inches, degrees F
## SMS:x = volumetric soil moisture at depth x inches, percent
eCodes = ['TAVG', 'TMAX', 'TMIN', 'TOBS', 'PREC', 'SNWD', 'WTEQ','STO','SMS']
eCodes = [s + '::value' for s in eCodes]
eCodes = [s.replace('STO', 'STO:-2:value,STO:-8:value,STO:-20:value') for s in eCodes]
eCodes = [s.replace('SMS', 'SMS:-2:value,SMS:-8:value,SMS:-20:value') for s in eCodes]
eCodes = ','.join(eCodes)

# Read in data from website API for each row in snow-meta.csv
master = ReadSnowData(ntwk.state[0], ntwk.site_id[0], eCodes)
for row in tqdm(ntwk.itertuples()): 
    temp = ReadSnowData(row.state, row.site_id, eCodes)
    if temp is not None:
        master = master.append(temp)
    else:
        continue

# Clean raw data - remove NA's, rename columns, and add meta data / alternate date formats
clean = master.dropna()
clean.rename(columns = {'temp avg (degf)':'tAvg',
                        'temp max (degf)':'tMax',
                        'temp min (degf)':'tMin',
                        'temp  (degf)':'t',
                        'precip accum (in)':'precipAccum',
                        'snow  (in)':'snow',
                        'snow water equiv (in)':'waterEquiv',
                        'soil temp  2in (degf)':'tSoil2',
                        'soil temp  8in (degf)':'tSoil8'}, inplace=True)
meta = ntwk[['state', 'site_name', 'latitude', 'longitude', 'elev_ft', 'county', 'huc', 'site_id']]
meta.rename(columns = {'site_name':'name', 
                       'latitude':'lat', 
                       'longitude':'long', 
                       'elev_ft':'elev', 
                       'site_id':'id'}, inplace=True)
clean = pd.merge(clean, meta)
clean = clean[clean['snow'].notnull()]
clean.insert(loc=0, column='md',    value=clean.date.str.extract(r'((?<=-)\d{2}-\d{2})', expand=False))
clean.insert(loc=0, column='day',   value=clean.date.str.extract(r'((?<=-)\d{2}$)',      expand=False))
clean.insert(loc=0, column='month', value=clean.date.str.extract(r'((?<=-)\d{2}(?=-))',  expand=False))
clean.insert(loc=0, column='year',  value=clean.date.str.extract(r'(\d{4}(?=-))',        expand=False))

# Export final CSV's
master.to('snow-raw.csv', index=False)
clean.to_csv('snow-clean.csv', index=False)