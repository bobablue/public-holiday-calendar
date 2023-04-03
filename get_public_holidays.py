import requests
import pandas as pd

#%% static data
countries = {'AU':'Australia','CN':'China','DE':'Germany','HK':'Hong Kong',
             'ID':'Indonesia','IN':'India','JP':'Japan','KR':'South Korea',
             'MY':'Malaysia','NZ':'New Zealand','PH':'Philippines','LK':'Sri Lanka',
             'SG':'Singapore','TH':'Thailand','TW':'Taiwan','GB':'United Kingdom',
             'VN':'Vietnam'}

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

#%% tidy up, keep only tidied columns (date, subject, description)
hols_df['Date'] = pd.to_datetime(hols_df['date']).dt.date
hols_df['Subject'] = '[' + hols_df['countryCode'].map(countries) + '] ' + hols_df['name']
hols_df = hols_df.rename(columns={'localName':'Description'})

hols_df = hols_df[['Date','Subject','Description']]

#%% export
hols_df.to_csv('Public Holidays.csv', encoding='utf-16', index=False)