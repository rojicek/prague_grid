# nacte archiv se Stravy a udela ze vsecho gpx soubory

import os
import pathlib
import time
import numpy as np
# import gpxpy
# import geopy
# from geopy.distance import geodesic
# from fit2gpx import Converter
from fit2gpx import StravaConverter
import os


import mytcx2gpx

import pandas as pd

# https://pypi.org/project/fit2gpx/

fit_folder_path = r'c:\Users\jiri\Documents\dev_code\Prague_grid\prague_grid\from_strava_2023-07-29'

# tcx input files (pro ostatni soubory neni treba - zna strukturu exportu ze stravy)
tcx_folder_path = os.path.join(fit_folder_path, 'activities')
# output folder for gpx files
gpx_folder_path = os.path.join(fit_folder_path, 'activities_processed_gpx')

# make sure output folder is empty
if not os.path.exists(gpx_folder_path):
    os.makedirs(gpx_folder_path)

if os.listdir(gpx_folder_path):
    print(f'{gpx_folder_path} neni prazdny!!')
    assert False

if True:
    strava_conv = StravaConverter(dir_in=fit_folder_path, dir_out=gpx_folder_path)

    # Step 2: Unzip the zipped files
    strava_conv.unzip_activities()

    # Step 3: Add metadata to existing GPX files and copy gpx files
    strava_conv.add_metadata_to_gpx()

    print('start actual conversion')
    # Step 4: Convert FIT to GPX
    strava_conv.strava_fit_to_gpx()

# tcx processing (added by me)
if True:
    for file in os.listdir(tcx_folder_path):
        if file.endswith('.tcx'):
            print(file)  # printing file name of desired extension
            full_tcx_name = os.path.join(tcx_folder_path, file)

            # remove whitespace
            inf = open(full_tcx_name)
            stripped_lines = [l.lstrip() for l in inf.readlines()]
            inf.close()

            # write the new, stripped lines to a file
            outf = open(full_tcx_name, 'w')
            outf.write("".join(stripped_lines))
            outf.close()

            gps_object = mytcx2gpx.TCX2GPX(tcx_path=full_tcx_name)
            gps_object.convert()

            # delete original tcx
            os.remove(full_tcx_name)

print('konec')