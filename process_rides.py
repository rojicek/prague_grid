# process gpx (export all points to hdf and json for js)

import os
import pathlib
import time
import numpy as np
import gpxpy
import geopy
from geopy.distance import geodesic
from bs4 import BeautifulSoup

import os


import pandas as pd

root_folder = r'c:\Users\jiri\Documents\dev_code\Prague_grid\prague_grid\rides'
js_folder_path = os.path.join(root_folder, 'processed_activities_js')
df_folder_path = os.path.join(root_folder, 'processed_activities_df')

# test that folders exists and are empty
for folder in [js_folder_path, df_folder_path]:
    if not os.path.exists(folder):
        os.makedirs(folder)


source_gpx_folder_path = r'c:\Users\jiri\Documents\dev_code\Prague_grid\prague_grid\from_strava\activities_processed_gpx'
flag_create_js_data = True

# key input parameter - jak daleko max muzou byt body od sebe
max_allowed_distance = 10


def process_gpx(gpx_file):
    # pro  javascript data - neni potreba pro dataframe
    d = {}
    i = 0

    d_orig = {}
    i_orig = 0

    df_i = pd.DataFrame(columns=['latitude', 'longitude'])

    with open(gpx_file, 'r') as gpx_file_handler:
        gpx = gpxpy.parse(gpx_file_handler)
        prev_point = geopy.Point(0, 0)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:

                    actual_point = geopy.Point(point.latitude, point.longitude)

                    if prev_point != geopy.Point(0, 0):

                        actual_distance = geodesic(prev_point, actual_point)

                        # need to interpolate
                        # mam krajni body, rozdelim je
                        diff_latitude = actual_point.latitude - prev_point.latitude
                        diff_longitude = actual_point.longitude - prev_point.longitude

                        if actual_distance.meters > max_allowed_distance:
                            for alpha in np.arange(0, 1, max_allowed_distance / actual_distance.meters):
                                # neni to uplne korektni, ale bude to spise hustsi nez neopak
                                interpolated_latitude = prev_point.latitude + alpha * diff_latitude
                                interpolated_longitute = prev_point.longitude + alpha * diff_longitude

                                # dvakrat totez
                                df_i = pd.concat([df_i, pd.DataFrame(
                                    [{'latitude': interpolated_latitude, 'longitude': interpolated_longitute}])])
                                if flag_create_js_data:
                                    d[i] = f"{interpolated_latitude}N,{interpolated_longitute}E"
                                    i = i + 1

                    # print ('*')
                    # pridej actual_point bod (casto bude 2x, ale to je jedno) - protoze to bude dalsi nasledujici bod
                    # 2 duplicitni zapisy
                    df_i = pd.concat(
                        [df_i, pd.DataFrame([{'latitude': actual_point.latitude, 'longitude': actual_point.longitude}])])
                    if flag_create_js_data:
                        d[i] = f"{actual_point.latitude}N,{actual_point.longitude}E"
                        i = i + 1
                        d_orig[i_orig] = f"{actual_point.latitude}N,{actual_point.longitude}E"
                        i_orig = i_orig + 1

                    # posunu predchozi bod
                    prev_point = geopy.Point(actual_point)
                    # print (actual_point)
                    # print (prev_point)
                    # print ('--------------------------------')

    df_i.reset_index(drop=True, inplace=True)
    return df_i, d, d_orig


for root, dirs, files in os.walk(source_gpx_folder_path):
    for i, file_name in enumerate(files):

        df_file_path = os.path.join(df_folder_path, file_name + '.h5')

        # test, jestli uz nemam vysledky
        if not os.path.isfile(df_file_path):
            full_source_path = os.path.join(root, file_name)

            # test jestli to neni virtualni jizda
            with open(full_source_path, 'r') as f:
                xml_data = f.read()

            # Passing the stored data inside
            # the beautifulsoup parser, storing
            # the returned object
            beautiful_data = BeautifulSoup(xml_data, "xml")
            ride_tag = beautiful_data.find_all('type')[0]
            if ride_tag.get_text().lower() == 'virtual ride':
                # nezpracovavam virtualni jizdy
                print(f'virtual {file_name} [{i}/{len(files)}]')
                continue


            print(f'{file_name} [{i}/{len(files)}]')

            df, d, d_orig = process_gpx(full_source_path)

            # write 3 files
            # store df
            df.to_hdf(df_file_path, key='data')

            # store js (mene dulezite)
            if flag_create_js_data:
                jsorig_file_path = os.path.join(js_folder_path, file_name + '.orig.js')
                with open(jsorig_file_path, 'w') as fo:
                    fo.write(str(d_orig))

                jsrich_file_path = os.path.join(js_folder_path, file_name + '.rich.js')
                with open(jsrich_file_path, 'w') as fr:
                    fr.write(str(d))

        else:
            print(f'uz mam {file_name} [{i}/{len(files)}]')


print('konec')