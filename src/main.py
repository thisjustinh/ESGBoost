import pandas as pd
import re
import json


def clean_pct(stat: str):
    m = re.search(r'\(.*?\)', str(stat))

    if m:
        new = m.group(0)
        new = re.sub('[(%)]', '', new)
        return new
    return stat


# Drop unnecessary columns
zips = pd.read_csv('data/zip.csv')
zips = zips.drop(columns=['zip'])

# Drop unnecessary columns
returns = pd.read_csv('data/returns.csv')
returns = returns.drop(columns=['lag0','lag1','lag2','lag3'])

# Drop NA rows
esg = pd.read_csv('data/esg.csv')

# Clean data
echo = pd.read_csv('data/echo.csv')
echo['minority_pct'] = echo['minority_pct'].apply(lambda x: re.sub(r'[%]', '', str(x)))
problems = ['primary_school','high_school','hs_diploma','some_college','bsba','income_l15','income_15_25','income_25_50','income_50_75','income_p75']
for problem in problems:
    echo[problem] = echo[problem].apply(clean_pct)


# Goal: Master CSV!
master = pd.merge(zips, esg, on='ticker')
master = pd.merge(master, echo, on='ticker')
master = pd.merge(master, returns, on='ticker')
master = master.dropna()
master.to_csv('data/master.csv', index=False)

# Name to Ticker
convert = [{row['longName']: row['ticker']} for index, row in master.iterrows()]
with open('data/convert.json', 'w') as f:
    f.write(json.dumps(convert))

# JSONs
master = master.set_index('longName')
master.to_json('data/longName.json', orient='index')
master = master.set_index('ticker')
master.to_json('data/ticker.json', orient='index')
