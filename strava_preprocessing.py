# nacte archiv se Stravy a udela ze vsecho gpx soubory

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

# https://pypi.org/project/fit2gpx/

fit_folder_path = r'c:\Users\jiri\Documents\dev_code\Prague_grid\prague_grid\rides'

# output folder for gpx files
gpx_folder_path = os.path.join(fit_folder_path, 'activities_gpx')


strava_conv = StravaConverter(dir_in=fit_folder_path, dir_out=gpx_folder_path)

# Step 2: Unzip the zipped files
strava_conv.unzip_activities()

# Step 3: Add metadata to existing GPX files and copy gpx files
strava_conv.add_metadata_to_gpx()

print('start actual conversion')
# Step 4: Convert FIT to GPX
strava_conv.strava_fit_to_gpx()

#todo: chybi tcx soubory z 2013/2014 ... chybi Rakousko, Lipot
# v Praze to ale zadny novy ctverec nebude
# 65 tcx souboru

print('konec')