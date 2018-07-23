def ReadSnowData(state, siteID, eCodes):

    # example:
    # https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customSingleStationReport/daily/start_of_period/1278:UT:SNTL%7Cid=%22%22%7Cname/POR_BEGIN,POR_END/TAVG::value,TMAX::value,TMIN::value,TOBS::value,PREC::value,SNWD::value,SNWDV::value,SNWDX::value,SNWDN::value,WTEQ::value,WTEQV::value,WTEQX::value,WTEQN::value,SMS:-2:value,SMS:-8:value,SMS:-20:value,STV::value,STX::value,STN::value,STO:-2:value,STO:-8:value,STO:-20:value
    # Note: POR stands for 'period of record'
    
    import urllib, re
    import pandas as pd
    
    def MultipleReplace(text, adict):
        rx = re.compile('|'.join(map(re.escape, adict)))
        def one_xlat(match):
            return adict[match.group(0)]
        return rx.sub(one_xlat, text)
    
    combined = siteID.split(':')[::-1]
    combined = combined[0] + ':' + state + ':' + combined[1]
    baseURL = 'https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customSingleStationReport/'
    fullURL = baseURL + 'daily/start_of_period/' + combined + '%7Cid=%22%22%7Cname/POR_BEGIN,POR_END/' + eCodes

    f = urllib.urlopen(fullURL)
    raw = f.read()
    lines = raw.split('\n')
    data = [i for i in lines if not re.compile('^#').search(i)]

    if data[1] != '':
        df = pd.DataFrame([s.split(',') for s in data[1:]])
        header = data[0].lower()
        subs = {'temperature':'temp', 'precipitation':'precip', 'equivalent':'equiv', 'moisture':'moist', 'accumulation':'accum',
                'minimum':'min', 'maximum':'max', 'average':'avg',
                'start of day values':'', 'observed':'', 'percent':'', 'air ':'', 'depth':'', '-':'', '^[ \t\r\n]+|[ \t\r\n]+$':''}
        header = MultipleReplace(header, subs)
        df.columns = header.split(',')
        df['id'] = pd.Series(siteID, index = df.index)
        return df
    else:
        return None