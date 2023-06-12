# process gpx (export all points)
import os
import pathlib
import time
import numpy as np
import gpxpy
import geopy
from geopy.distance import geodesic
from fit2gpx import Converter
from fit2gpx import StravaConverter
import os

import pandas as pd

#gpx_file = open(r'c:\Users\jiri\Documents\dev_code\Prague_grid\prague_grid\output\Besr23.gpx', 'r')
fit_folder_path = r'c:\Users\jiri\Documents\dev_code\Prague_grid\prague_grid\rides\activities_gpx'
flag_create_js_data = True

max_allowed_distance = 100


def process_gpx(gpx_file):
    # pro  javascript data - neni potreba pro dataframe
    d = {}
    i = 0

    d_orig = {}
    i_orig = 0

    df = pd.DataFrame(columns=['latitude', 'longitude'])
    gpx = gpxpy.parse(gpx_file)

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
                            df = pd.concat([df, pd.DataFrame(
                                [{'latitude': interpolated_latitude, 'longitude': interpolated_longitute}])])
                            if flag_create_js_data:
                                d[i] = f"{interpolated_latitude}N,{interpolated_longitute}E"
                                i = i + 1

                # print ('*')
                # pridej actual_point bod (casto bude 2x, ale to je jedno) - protoze to bude dalsi nasledujici bod
                # 2 duplicitni zapisy
                df = pd.concat(
                    [df, pd.DataFrame([{'latitude': actual_point.latitude, 'longitude': actual_point.longitude}])])
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
    return df, d, d_orig


for root, dirs, files in os.walk(fit_folder_path):
    for file_name in files:
        full_path = os.path.join(root,file_name)
        print(full_path)
        df, d, d_orig = process_gpx (full_path)
        xxxx=0


# loop over gpx files
# if flag_create_js_data:
#     with open(r'c:\Users\jiri\Documents\dev_code\Prague_grid\prague_grid\output\besr-edited.js.data', 'w') as f:
#         f.write(str(d))
#     with open(r'c:\Users\jiri\Documents\dev_code\Prague_grid\prague_grid\output\besr-orig.js.data', 'w') as f:
#         f.write(str(d_orig))
#
print('konec')