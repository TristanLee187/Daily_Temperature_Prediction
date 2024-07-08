from datetime import datetime
from meteostat import Point, Daily
import pandas as pd

# set the start and end dates
start = datetime(2000, 1, 1)
end = datetime(2024, 3, 4)

# create Points for Central Park, Midway Airport, Bergstrom Airport, and Miami
central_park = Point(40.779447, -73.96906), 'ny'
midway = Point(41.78597, -87.75242), 'chicago'
bergstrom = Point(30.1953, -97.6667), 'austin'
miami = Point(25.7617, -80.1918), 'miami'
points = [central_park, midway, bergstrom, miami]

# get history data
total_data = pd.DataFrame()
for point, loc in points:
    data = Daily(point, start, end)
    data = data.fetch()

    # convert to Fahrenheit
    data['tavg'] = 1.8 * data['tavg'] + 32
    data['tmin'] = 1.8 * data['tmin'] + 32
    data['tmax'] = 1.8 * data['tmax'] + 32

    # convert to inches
    data['prcp'] = data['prcp'] / 25.4

    # export
    data.to_csv(f'{loc}/{loc}_meteostat.csv')