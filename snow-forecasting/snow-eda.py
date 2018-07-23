# Load required modules and data
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
import pandas as pd
import numpy as np

os.chdir('/home/addison/Documents/professional/data/snow-forecasting')
clean = pd.read_csv('snow-clean')

# Plotting trends
utah = clean.query("state == 'UT'")
mostData = clean.query("state == 'WA' | state == 'CA' | state == 'AK'")
del clean
mostData = utah[utah.id.isin(np.unique(utah.id)[:10])] 
hasSnow = mostData.query('snow > 0')
del utah
del mostData

# Group data into winters (i.e. periods of continuous snow coverage)
# Filter all non-zero values and then group by consecutive index (and site ID)
# About 54% of data is nonzero snow
hasSnow = mostData.query('snow > 0')
hasSnow.reset_index(level=0, inplace=True)
hasSnow.rename(columns={'index': 'entry'}, inplace=True)
hasSnow.loc[max(hasSnow.index)+1, :] = None
hasSnow = hasSnow.assign(entry_s = hasSnow.entry.shift(-1))
hasSnow = hasSnow[1:-1] # Remove the NaN rows from shifting
hasSnow = hasSnow.assign(consec = (hasSnow.entry + 1) == hasSnow.entry_s) 

# Determine streaks of greater than 30 consecutive days
gaps = np.array(np.where(hasSnow.consec == False))
gaps = np.append(np.array([0]), gaps)
streaks = np.diff(gaps)
winters = [(g+1, g+s, s)  for g,s in zip(gaps, streaks) if s > 30] # start index, end index, and length for each streak
winters[0] = (0, winters[0][1], winters[0][2]) # manually start from 0 index (instead of 1)
iWinter = np.concatenate([np.repeat(i, w[2]) for i,w in zip(np.arange(1, len(winters) + 1), winters)]) # repeat winter ID for the length of streak

keep = np.concatenate([np.arange(i[0], i[1], 1) for i in winters]) 
hasSnow = hasSnow[hasSnow.index.isin(keep)] 
hasSnow = hasSnow.assign(winter = iWinter[:-1])
smaller = hasSnow[['md', 'id', 'consec']]

res = pd.DataFrame(winters)
res = res.assign(winter = np.arange(1, len(winters) + 1))
res.columns = ['start', 'end', 'days', 'winter']
res = pd.merge(res, hasSnow[['winter', 'id', 'state', 'name', 'lat', 'long', 'elev', 'county', 'huc']]).drop_duplicates()
# multiple sites for same winter: 10, 20, 31, 43, 86, 117, 100
# add length of the winter and max depth

hasSnow = hasSnow.assign(plotDate = np.where(hasSnow.month < 9, 
                                             pd.to_datetime('1971-' + hasSnow.md.map(str), errors='coerce'),
                                             pd.to_datetime('1970-' + hasSnow.md.map(str), errors='coerce')))
hasSnow = hasSnow[hasSnow.plotDate.notnull()]
ggplot(hasSnow, aes('plotDate', 'snow', group = 'winter', color = 'name')) +\
    theme_bw() +\
    geom_line(size = 1.5, alpha = 0.6) +\
    scale_x_date(labels='%b') +\
    xlab('Month') +\
    ylab('Snow Depth (in)')

 
# Filtering
    # Remove incomplete winters
    # Check spikes > 100 feet (Holts-Winters, exponential smoothing, ARIMA)
# Extract the max depth and first melt date for each season
# Calculate length/depth ratio
# Add meta data into the new data frame version
# Get KG climate zone for each (long, lat) location from R
# PCA on shape of snow curves?
# Overlay temperature plot with snow to look for rapid fall off
