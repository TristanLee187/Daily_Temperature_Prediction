from world_weather_online_api_key import world_weather_online_api_key
import requests
from datetime import date, timedelta
import pandas as pd

WWO_API_ENDPOINT = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx'

austin_lat_long = (30.1953, -97.6667)
miami_lat_long = (25.7617, -80.1918)

# get daily data
params = {
    'q': '',
    'date': '',
    'enddate': '',
    'tp': 24,
    'format': 'JSON',
    'key': world_weather_online_api_key
}

for locs in [austin_lat_long, miami_lat_long]:
    df = pd.DataFrame(columns = ['date', 'maxtempF'])
    params['q'] = ','.join(map(str, austin_lat_long))
    # need to query one month at a time since that's the limit of the API call
    for i in range(12):
        month = 3+i
        if month != 12:
            year = 2023 + (0 if month < 12 else 1)
            month = month if month < 12 else month - 12
            date1, date2 = date(year, month, 1), date(year, month+1, 1) - timedelta(days=1)
        else:
            date1, date2 = date(2023, month, 1), date(2024, 1, 1) - timedelta(days=1)
        
        params['date'] = str(date1)
        params['enddate'] = str(date2)

        try:
            response = requests.get(WWO_API_ENDPOINT, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            data = response.json()
            weather = data['data']['weather']
            month_df = {
                'date': [day['date'] for day in weather],
                'maxtempF': [day['maxtempF'] for day in weather]
            }
            df = pd.concat([df, pd.DataFrame.from_dict(month_df)])
        except requests.exceptions.RequestException as e:
            print("Error fetching weather data:", e)
    if locs[0] > 30:
        df.to_csv('austin_wwo.csv', index=False)
    else:
        df.to_csv('miami_wwo.csv', index=False)