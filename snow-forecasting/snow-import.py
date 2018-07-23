# Load required modules
import os
import pandas as pd
from tqdm import tqdm
from ReadSnowData import ReadSnowData # Check Spyder folder path if error

# Import meta data to pass to search queries
os.chdir('C:/Users/User/Documents/personal/outdoors/backpacking/snow-forecasting')
ntwk = pd.read_csv('snowMeta.csv')
eCodes = ['TAVG', 'TMAX', 'TMIN', 'TOBS', 'PREC', 'SNWD', 'WTEQ','STO','SMS']
eCodes = [s + '::value' for s in eCodes]
eCodes = [s.replace('STO', 'STO:-2:value,STO:-8:value,STO:-20:value') for s in eCodes]
eCodes = [s.replace('SMS', 'SMS:-2:value,SMS:-8:value,SMS:-20:value') for s in eCodes]
eCodes = ','.join(eCodes)

# Read in data from website
first = True
for row in tqdm(ntwk.itertuples()): 
    temp = ReadSnowData(row.state, row.site_id, eCodes)
    if temp is not None:
        if not first:
            master = master.append(temp)
        else:
            master = temp
            first = False
    else:
        continue

# Clean raw data
clean = master.dropna()
clean.rename(columns = {'temp avg (degf)':'tAvg',
                        'temp max (degf)':'tMax',
                        'temp min (degf)':'tMin',
                        'temp  (degf)':'t',
                        'precip accum (in)':'precipAccum',
                        'snow  (in)':'snow',
                        'snow water equiv (in)':'waterEquiv',
                        'soil temp  2in (degf)':'tSoil2',
                        'soil temp  8in (degf)':'tSoil8'}, inplace = True)
meta = ntwk[['state', 'site_name', 'latitude', 'longitude', 'elev_ft', 'county', 'huc', 'site_id']]
meta.rename(columns = {'site_name':'name', 'latitude':'lat', 'longitude':'long', 'elev_ft':'elev', 'site_id':'id'}, inplace = True)
clean = pd.merge(clean, meta)
clean = clean[clean['snow'].notnull()]
clean.insert(loc=0, column='md', value=clean.date.str.extract(r'((?<=-)\d{2}-\d{2})', expand=False))
clean.insert(loc=0, column='day', value=clean.date.str.extract(r'((?<=-)\d{2}$)', expand=False))
clean.insert(loc=0, column='month', value=clean.date.str.extract(r'((?<=-)\d{2}(?=-))', expand=False))
clean.insert(loc=0, column='year', value=clean.date.str.extract(r'(\d{4}(?=-))', expand=False))
clean.to_csv('snow-clean', index = False)
