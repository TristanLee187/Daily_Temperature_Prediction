import pandas as pd

# the different city names
locs = ['austin', 'chicago', 'miami', 'ny']

# the column names of the final aggregated data
final_column_names = ['date', 'tmax', 'prec', 'pres', 'cloud', 'rhum']

for loc in locs:
    # init the final aggregated df
    final_df = pd.DataFrame(columns = final_column_names)

    # read meteostat, noaa, and open meteo data, and filter for just the data we need
    prefix = f'{loc}/{loc}'
    meteostat_df = pd.read_csv(f'{prefix}_meteostat.csv')
    meteostat_df = meteostat_df[['time', 'tmax', 'prcp', 'pres']]
    meteostat_df.columns = ['date', 'tmax', 'prec', 'pres']
    final_df = pd.concat([final_df, meteostat_df])

    noaa_df = pd.read_csv(f'{prefix}_noaa.csv')
    noaa_df.columns = ['date', 'prec', 'tmax']
    final_df = pd.concat([final_df, noaa_df])

    open_meteo_df = pd.read_csv(f'{prefix}_open_meteo_daily.csv')
    final_df = pd.concat([final_df, open_meteo_df])

    # read the other data, which is based on the location
    if loc in ['austin', 'miami']:
        other_df = pd.read_csv(f'{prefix}_wwo.csv')
        other_df.columns = ['date', 'tmax']
    else:
        other_df = pd.read_csv(f'{prefix}_visualcrossing.csv')
        other_df = other_df[['datetime', 'tempmax', 'humidity', 'precip', 'sealevelpressure', 'cloudcover']]
        other_df.columns = ['date', 'tmax', 'rhum', 'prec', 'pres', 'cloud']
    final_df = pd.concat([final_df, other_df])

    # aggregate the different data into a single table by taking averages
    # of old columns
    final_df = final_df.groupby(by='date').agg(
        {col: 'mean' for col in final_column_names[1:]}
    )

    # export
    final_df.to_csv(f'{prefix}_all_data.csv')
