import re
from urllib.request import urlopen
import pandas as pd
from MultipleReplace import MultipleReplace

def ReadSnowData(state, siteID, eCodes):

    """ Download snow and weather data from Dept of Agriculture's API.

    Visit https://wcc.sc.egov.usda.gov/reportGenerator/ to see the form for generating URL requests. 
    Note that the Department has made small changes to the URL format in the past, so the exact
    formulation in this function may become deprecated in the future.

    Parameters
    ----------
    state : str
      The standard two letter abbreviation
    siteID : str
      ID code from snow-meta.csv file which for most cases will be of the form 'SNTL:xxxx'
    eCodes : list of str
      Capital letter variable abbreviations defined by the API 

    Returns
    -------
    pandas.DataFrame
        Dataframe containing all variables specified in `eCodes` for the given `state` and `siteID`
    """
    
    # Generate request URL and read raw data
    urlID = 'id=%22{}%22%20AND%20state=%22{}'.format(siteID.split(':')[-1], state)
    baseURL = 'https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customSingleStationReport/daily/start_of_period/'
    fullURL = baseURL + urlID + '%22%20AND%20outServiceDate=%222100-01-01%22%7Cname/POR_BEGIN,POR_END/' + eCodes
    f = urlopen(fullURL)
    raw = f.read().decode('utf-8')
    f.close()

    # Split text into lines and remove all headers starting with '#'
    lines = raw.split('\n')
    data = [i for i in lines if not re.compile('^#').search(i)]

    if data[0] is not '':
        df = pd.DataFrame([s.split(',') for s in data[1:]])
        header = data[0].lower()
        subs = {'temperature':'temp', 'precipitation':'precip', 'equivalent':'equiv', 'moisture':'moist', 'accumulation':'accum',
                'minimum':'min', 'maximum':'max', 'average':'avg',
                'start of day values':'', 'observed':'', 'percent':'', 'air ':'', 'depth':'', '-':'', '^[ \t\r\n]+|[ \t\r\n]+$':''}
        header = MultipleReplace(header, subs)
        df.columns = header.split(',')
        df['id'] = pd.Series(siteID, index=df.index)
        return df
    else:
        return None