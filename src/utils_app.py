import json
import requests

import numpy as np
import pandas as pd
import sys
sys.path.append('./')

def get_sim_data():
    f = open('sim_data.json')
    data = json.load(f)
    f.close()
    forecast_df = pd.DataFrame(data['forecast'])[:24]
    forecast_df['datetime'] = pd.to_datetime(forecast_df['datetime'])
    forecast_df['date'] = forecast_df['datetime'].dt.date
    forecast_df['hour'] = forecast_df['datetime'].dt.hour
    forecast_df['price'] = np.random.randint(150,270, len(forecast_df))
    forecast_df['Dollar per carbon'] = forecast_df['price']/forecast_df['carbonIntensity']
    return forecast_df

def request_data(url, headers):
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    forecast_df = pd.DataFrame(data['forecast'])[:24]
    forecast_df['datetime'] = pd.to_datetime(forecast_df['datetime'])
    forecast_df['date'] = forecast_df['datetime'].dt.date
    forecast_df['hour'] = forecast_df['datetime'].dt.hour
    forecast_df['price'] = np.random.randint(150,270, len(forecast_df))
    forecast_df['Dollar per carbon'] = forecast_df['price']/forecast_df['carbonIntensity']
    return forecast_df