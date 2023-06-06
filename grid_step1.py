# prague grid

import json
import pandas as pd
import numpy as np
import geopy
import math
import os
import pathlib
import time


import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic

geo_locator = geopy.Nominatim(user_agent='prague_grid')

df_points = pd.DataFrame({'ix': pd.Series(dtype='int'),
                          'iy': pd.Series(dtype='int'),
                          'latitude': pd.Series(dtype='float'),
                          'longitude': pd.Series(dtype='float'),
                          'state': pd.Series(dtype='string')})

square_distance = 200  # m

# vnejsi ctverec okolo Prahy
outer_min_latitude = 49.9
outer_min_longitude = 14.2
outer_max_latitude = 50.2
outer_max_longitude = 14.8

# ctverec urcite uvnitr Prahy
inner_min_latitude = 50.03
inner_min_longitude = 14.32
inner_max_latitude = 50.11
inner_max_longitude = 14.42

inner_count = 0

# indexy v mem gridu abych snaze nasel souseda
ix = 0
iy = 0

# zacnu v SW rohu (lon/lat jsou minimalni)
actual_point = geopy.Point(latitude=outer_min_latitude, longitude=outer_min_longitude)

while actual_point.latitude <= outer_max_latitude:
    print(
        f'{round(100 * (outer_max_latitude - actual_point.latitude) / (outer_max_latitude - outer_min_latitude), 1)}%')
    actual_point.longitude = outer_min_longitude
    while actual_point.longitude <= outer_max_longitude:

        # calc other rect points
        if inner_min_latitude < actual_point.latitude < inner_max_latitude and \
                inner_min_longitude < actual_point.longitude < inner_max_longitude:

            # vnitrni Praha
            df_points = pd.concat([df_points, pd.DataFrame([{'ix': ix, 'iy': iy,
                                                             'latitude': actual_point.latitude,
                                                             'longitude': actual_point.longitude,
                                                             'state': 'Praha'}])])
            inner_count = inner_count + 1

        else:  # need check OSM
            osm_sucessfully_read = False
            while not osm_sucessfully_read:
                try:
                    r = geo_locator.reverse(actual_point)
                    if 'address' in r.raw.keys():
                        osm_sucessfully_read = True
                except Exception:
                    print('API failed, repeating')
                    time.sleep(2)

            df_points = pd.concat([df_points, pd.DataFrame([{'ix': ix, 'iy': iy,
                                                             'latitude': actual_point.latitude,
                                                             'longitude': actual_point.longitude,
                                                             'state': str(r.raw['address']['state'])}])])

            # move point east
        actual_point = geopy.distance.distance(meters=square_distance).destination(actual_point, bearing=90)
        # posunu index
        ix = ix + 1

    # move point north
    actual_point = geopy.distance.distance(meters=square_distance).destination(actual_point, bearing=0)
    # posunu index a resetuji index x
    iy = iy + 1
    ix = 0

df_points.reset_index(inplace=True, drop=True)

total_points = df_points.shape[0]
total_points_in_prague = df_points[df_points['state'].str.lower() == 'praha'].shape[0]

print(f'Krok: {square_distance}')
print(f'Počet bodů: {total_points}')
print(f'Počet bodů v Praze: {total_points_in_prague}, {round(100 * total_points_in_prague / total_points, 2)}%')
print(f'Počet bodů ve vnitřní Praze: {inner_count}')

# /content/drive/My Drive/dev/Praha_grid/
root_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), 'output')

file_name_csv = os.path.join(root_folder, f'grid_{str(square_distance).zfill(5)}.csv')
file_name_hdf = os.path.join(root_folder, f'grid_{str(square_distance).zfill(5)}.hdf')
file_name_txt = os.path.join(root_folder, f'grid_{str(square_distance).zfill(5)}.txt')

df_points.to_csv(file_name_csv)
df_points.to_hdf(file_name_hdf, key='data')

# zapis info
with open(file_name_txt, 'w', encoding='utf-8') as f:
    f.write(f'Krok: {square_distance}\n')
    f.write(f'Počet bodů: {total_points}\n')
    f.write(f'Počet bodů v Praze: {total_points_in_prague}, {round(100 * total_points_in_prague / total_points, 2)}%\n')
    f.write(f'Počet bodů ve vnitřní Praze: {inner_count}\n')

