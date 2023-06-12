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

#gpx_file = open(r'c:\Users\jiri\Documents\dev_code\Prague_grid\prague_grid\output\Besr23.gpx', 'r')
fit_folder_path = r'c:\Users\jiri\Documents\dev_code\Prague_grid\prague_grid\rides'

strava_conv = StravaConverter(dir_in=fit_folder_path)

# Step 2: Unzip the zipped files
strava_conv.unzip_activities()

# Step 3: Add metadata to existing GPX files
strava_conv.add_metadata_to_gpx()

# Step 4: Convert FIT to GPX
strava_conv.strava_fit_to_gpx()

print('konec')