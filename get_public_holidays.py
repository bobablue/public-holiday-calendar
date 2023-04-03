import requests
import pandas as pd

#%% static data
countries = {'AU':'Australia','CN':'China','DE':'Germany','HK':'Hong Kong',
             'ID':'Indonesia','IN':'India','JP':'Japan','KR':'South Korea',
             'MY':'Malaysia','NZ':'New Zealand','PH':'Philippines','LK':'Sri Lanka',
             'SG':'Singapore','TH':'Thailand','TW':'Taiwan','GB':'United Kingdom',
             'VN':'Vietnam'}

fields = {'countryCode':'Country Code','date':'Date',
          'localName':'Local Name','name':'Name','types':'Types'}

#%% url and params (https://date.nager.at/)
url_base = 'https://date.nager.at/api/v3/PublicHolidays/2023/country'

#%% get data
hols = {}
for code, cty in countries.items():
    response = requests.get(url=url_base.replace('country',code))
    if response.content:
        hols[cty] = response.json()
    else:
        print(f"[Not available] {cty}")

#%% pass json data to dataframe
hols_df = pd.DataFrame()
for cty in hols.keys():
    hols_df = pd.concat([hols_df, pd.DataFrame(hols[cty])])

# keep only selected columns, tidy up format
hols_df = hols_df[list(fields.keys())].rename(columns=fields)
hols_df['Country'] = hols_df['Country Code'].map(countries)
hols_df['Date'] = pd.to_datetime(hols_df['Date']).dt.date

# single col combining country and holiday name
hols_df['Full Info'] = '[' + hols_df['Country'] + '] ' + hols_df['Name']

#%% export
hols_df.to_csv('Public Holidays.csv', encoding='utf-8', index=False)