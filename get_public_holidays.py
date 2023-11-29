"""fetch public holiodays of selected countries from API and save as flat file."""
import requests
import pandas as pd

#%% static data (https://date.nager.at/)
meta = {'url':'https://date.nager.at/api/v3/PublicHolidays/{year}/{country}',
        'year':'2024',
        'data_keep':['date','name','localName','countryCode'],
        'countries':{'AU':'Australia', 'CN':'China', 'DE':'Germany', 'HK':'Hong Kong',
                     'ID':'Indonesia', 'IN':'India', 'JP':'Japan', 'KR':'South Korea',
                     'MY':'Malaysia', 'NZ':'New Zealand', 'PH':'Philippines', 'LK':'Sri Lanka',
                     'SG':'Singapore', 'TH':'Thailand', 'TW':'Taiwan', 'GB':'United Kingdom',
                     'VN':'Vietnam'}}

meta['url'] = meta['url'].replace('{year}', meta['year'])

#%% get data
hols = {}
for code, cty in meta['countries'].items():
    response = requests.get(url=meta['url'].replace('{country}',code))
    if response.content:
        hols[cty] = response.json()

        # keep only selected json data
        for i in enumerate(hols[cty]):
            hols[cty][i[0]] = {k:v for k,v in hols[cty][i[0]].items() if k in meta['data_keep']}

    else:
        print(f"[Not available] {cty}")

#%% pass json data to dataframe
hols_df = pd.DataFrame()
for cty in list(hols):
    hols_df = pd.concat([hols_df, pd.DataFrame(hols[cty])])

#%% tidy up, keep only tidied columns (date, subject, description)
hols_df['Date'] = pd.to_datetime(hols_df['date']).dt.date
hols_df['Subject'] = '[' + hols_df['countryCode'].map(meta['countries']) + '] ' + hols_df['name']
hols_df = hols_df.rename(columns={'localName':'Description'})

hols_df = hols_df[['Date','Subject','Description']]
hols_df = hols_df.drop_duplicates().reset_index(drop=True)

#%% export
hols_df.to_csv(f"Public Holidays_{meta['year']}.csv", encoding='utf-8', index=False)