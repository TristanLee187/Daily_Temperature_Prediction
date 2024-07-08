import pandas as pd

# df is a table read that contains the hourly data given by Open Meteo
# aggregate the hourly data into daily data
def group_df_by_date(df):
    grouped_df = df.groupby(
        pd.to_datetime(df['time']).dt.date
    ).agg(
        {'temperature_2m (°C)': 'max', 
         'relative_humidity_2m (%)': 'mean', 
         'precipitation (mm)': 'sum', 
         'surface_pressure (hPa)': 'mean', 
         'cloud_cover (%)': 'mean'}
    ).reset_index()
    
    grouped_df.columns = [
        'date', 'tmax', 'rhum', 'prec', 'pres', 'cloud'
    ]

    # convert to Fahrenheit
    grouped_df['tmax'] = 1.8 * grouped_df['tmax'] + 32

    # convert to inches
    grouped_df['prec'] = grouped_df['prec'] / 25.4
    return grouped_df

locs = ['austin', 'chicago', 'miami', 'ny']

for loc in locs:
    df = pd.read_csv(f'archive/{loc}_open_meteo.csv')
    grouped_df = group_df_by_date(df)
    grouped_df.to_csv(f'{loc}/{loc}_open_meteo_daily.csv', index=False)