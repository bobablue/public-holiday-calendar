"""fetch public holiodays of selected countries from Google API and save as flat file."""
import os
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

#%% static data
meta = {'url':'https://www.googleapis.com/calendar/v3/calendars/en.{cty}%23holiday%40group.v.calendar.google.com/events?',

        'url_params':{'key':open('config/google_api_key.txt', 'r').read()},

        'countries':{'australian':'Australia', 'china': 'China', 'german':'Germany', 'hong_kong':'Hong Kong',
                     'indonesian':'Indonesia', 'indian':'India', 'japanese':'Japan',
                     'malaysia':'Malaysia', 'new_zealand':'New Zealand', 'philippines':'Philippines',
                     'south_korea':'South Korea', 'lk':'Sri Lanka', 'singapore':'Singapore',
                     'th':'Thailand', 'taiwan':'Taiwan',
                     'uk':'United Kingdom', 'vietnamese':'Vietnam'}}

#%% functions
#%%
def get_data(country):
    response = requests.get(url=meta['url'].replace('{cty}',country), params=meta['url_params']).json()
    if 'error' in response:
        print(f"Error in country code: {country}")
        return(None)
    else:
        print(f"[{meta['countries'][country]}] done")
    return(response)

#%%
def pool_getdata(list_countries):
    data = {}
    with ThreadPoolExecutor(max_workers=min(os.cpu_count()*10, len(list_countries))) as executor:
        for i,j in list_countries.items():
            data[j] = executor.submit(get_data, i)
    data = {k:v.result() for k,v in data.items()}
    return(data)

#%%
def extract_data(json_obj):
    data = []
    for cty in json_obj:
        for hol in json_obj[cty]['items']:
            if hol['description']=='Public holiday':
                data.append([cty, hol['summary'],
                             [x.date() for x in pd.date_range(start=hol['start']['date'],
                                                              end=hol['end']['date'],
                                                              inclusive='left')]])

    data = pd.DataFrame(data, columns=['Country','Public Holiday','Date']).explode(['Date'])
    data['Calendar Title'] = '[' + data['Country'] + '] ' + data['Public Holiday']
    return(data)

#%% get data
data = {}
data['raw'] = pool_getdata(meta['countries'])
data['clean'] = extract_data(data['raw'])

#%% export
data['clean'].to_csv('Public Holidays.csv', encoding='utf-8', index=False)