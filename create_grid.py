# prague grid
import datetime
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

# velikost ctverce gridu
square_distance = 3000  # m

# vnejsi ctverec okolo Prahy
outer_min_latitude = 49.9
outer_min_longitude = 14.2
outer_max_latitude = 50.2
outer_max_longitude = 14.8

# ctverec urcite uvnitr Prahy
# jen pro zrychleni
inner_min_latitude = 50.03
inner_min_longitude = 14.32
inner_max_latitude = 50.11
inner_max_longitude = 14.63

# pocet bodu uvnitr Prahy
inner_count = 0

# indexy v mem gridu abych snaze nasel souseda
ix = 0
iy = 0

total_start = time.time()
last_time = total_start
print(f'start: {datetime.datetime.now()}')

# zacnu v SW rohu (lon/lat jsou minima)
sw_corner = geopy.Point(latitude=outer_min_latitude, longitude=outer_min_longitude)

se_corner = geopy.Point(latitude=outer_min_latitude, longitude=outer_max_longitude)
nw_corner = geopy.Point(latitude=outer_max_latitude, longitude=outer_min_longitude)

latitude_dist_iy = int(geopy.distance.distance(sw_corner, nw_corner).meters / square_distance) + 1  # index y
longitude_dist_ix = int(geopy.distance.distance(sw_corner, se_corner).meters / square_distance) + 1  # index x


for ix in range(0, longitude_dist_ix):

    # mezi smyckami jen tisk casu
    t_elapsed = time.time() - last_time
    t_elapsed_total = time.time() - total_start
    done_percent = ix/longitude_dist_ix
    if done_percent > 0:
        eta = datetime.datetime.now() + datetime.timedelta(seconds=(1-done_percent) * t_elapsed_total / done_percent)
    else:
        eta = 'NA'

    last_time = time.time()
    print(f'hotovo: {round(100 * done_percent, 1)}%, posledni: {round(t_elapsed, 1)}s, eta: {eta}')

    for iy in range(0, latitude_dist_iy):

        # na vychod
        actual_point_1 = geopy.distance.distance(meters=ix*square_distance).destination(sw_corner, bearing=90)
        # a na sever
        actual_point = geopy.distance.distance(meters=iy * square_distance).destination(actual_point_1, bearing=0)

        if (inner_min_latitude < actual_point.latitude < inner_max_latitude and \
                inner_min_longitude < actual_point.longitude < inner_max_longitude):
            # vnitrni Praha
            known_state = 'Praha'

            # jen pro report
            inner_count = inner_count + 1

        else:  # need check OSM
            osm_sucessfully_read = False
            known_state = 'nevim'
            while not osm_sucessfully_read:
                try:
                    r = geo_locator.reverse(actual_point)
                    if 'address' in r.raw.keys():
                        known_state = str(r.raw['address']['state'])
                        osm_sucessfully_read = True
                except Exception:
                    print('API failed, repeating')
                    time.sleep(2)

        df_points = pd.concat([df_points, pd.DataFrame([{'ix': ix, 'iy': iy,
                                                         'latitude': actual_point.latitude,
                                                         'longitude': actual_point.longitude,
                                                         'state': known_state}])])


df_points.reset_index(inplace=True, drop=True)

total_points = df_points.shape[0]
total_points_in_prague = df_points[df_points['state'].str.lower() == 'praha'].shape[0]

print(f'Krok: {square_distance}')
print(f'Počet bodů: {total_points}')
print(f'Počet bodů v Praze: {total_points_in_prague}, {round(100 * total_points_in_prague / total_points, 2)}%')
print(f'Počet bodů ve vnitřní Praze: {inner_count}')

# post processing - zahodim vse, co neni v Praze

# /content/drive/My Drive/dev/Praha_grid/
root_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), 'output')

file_name_csv = os.path.join(root_folder, f'grid_{str(square_distance).zfill(5)}.csv')
file_name_hdf = os.path.join(root_folder, f'grid_{str(square_distance).zfill(5)}.hdf')
file_name_txt = os.path.join(root_folder, f'grid_{str(square_distance).zfill(5)}.txt')

df_points.to_csv(file_name_csv)
df_points.to_hdf(file_name_hdf, key='data')

print(f'konec: {datetime.datetime.now()}')

# integrity test
max_ix = df_points['ix'].max()
max_iy = df_points['iy'].max()
add_info = ''

if len(np.unique(df_points[['ix', 'iy']], axis=0)) != len(df_points):
    print('INDEXY NEJSOU UNIKATNI!!')
    add_info = f'{add_info}\nindexy nejsou unikatni'

if (max_ix+1) * (max_iy+1) != len(df_points):
    print('NESEDI POCET BODU!!')
    add_info = f'{add_info}\nnesedi pocet bodu: {max_ix+1} * {max_iy+1} == {len(df_points)}'

# zapis info
with open(file_name_txt, 'w', encoding='utf-8') as f:
    f.write(f'Krok: {square_distance}\n')
    f.write(f'Počet bodů: {total_points}\n')
    f.write(f'Počet bodů v Praze: {total_points_in_prague}, {round(100 * total_points_in_prague / total_points, 2)}%\n')
    f.write(f'Počet bodů ve vnitřní Praze: {inner_count}\n')
    f.write(f'Doba výpočtu: {round(time.time()-total_start, 0)}s\n')
    f.write(f'{add_info}')

print('zapsano!')
