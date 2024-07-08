import pandas as pd

df = pd.read_csv('all_locations_noaa.csv')

city_station_mapping = {
    'ny': 'USW00094728',
    'chicago': 'USW00014819',
    'austin': 'USW00013904',
    'miami': 'USC00085667'
}

# split the all_locations table into 4 separate tables for each city, 
# plus keep just a few of the columns
for city in city_station_mapping:
    local_df = df[df['STATION'] == city_station_mapping[city]][
        ['DATE', 'PRCP', 'TMAX']
    ]
    local_df.to_csv(f'{city}_noaa.csv', index=False)
