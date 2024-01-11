import os

import pandas as pd
import requests
import sys


def getGoogleSeet(out_dir, url):
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(out_dir, 'solutions.csv')
        with open(filepath, 'wb') as f:
            f.write(response.content)
        df = pd.read_csv(filepath)
        print(df)
    else:
        print(f'Error downloading Google Sheet: {response.status_code}')
        sys.exit(1)


def get_tsp_from_drive():
    out_dir = 'TSP/'
    url = f'https://docs.google.com/spreadsheets/d/1WJy2-W-i1eL0LMEMbGjxhqD-LnSUzdcbV3nv7On_FUU/export?format=csv'
    getGoogleSeet(out_dir, url)


def get_fl_from_drive():
    out_dir = 'FL/'
    url = f'https://docs.google.com/spreadsheets/d/1TvexBbkXkAd9gEopAlUBwsXQnyRYyeeB5bEG9xAg0TI/export?format=csv'
    getGoogleSeet(out_dir, url)
