import requests
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup
import pandas as pd

data = None
for page in tqdm(range(1, 10000)):
    url = f'https://reestr.rublacklist.net/?status=1&gov=all&paginate_by=500&page={page}'
    r = requests.get(url)
    if r.status_code == 404:
        print('404')
        break
    if data is None:
        data = pd.read_html(r.text)[0]
    else:
        try:
            data = pd.concat([data, pd.read_html(r.text)[0]])
        except Exception as e:
            print(e)

data.drop(['Unnamed: 0', 'Unnamed: 3'], axis=1, inplace=True)
data.columns = ['date', 'site', 'who_blocked', 'count_of_blocked_domains']

# create year and month columns
data.date = pd.to_datetime(data.date)
data['year'] = data.date.dt.year
data['month'] = data.date.dt.month

data.reset_index(inplace=True)
data.drop('index', axis=1, inplace=True)

data.to_csv('scraped_blocking_data.csv')