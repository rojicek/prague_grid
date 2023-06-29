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

# spejchar
# test_point = geopy.Point(latitude=50.0966533, longitude=14.4081531)

# badeniho
test_point = geopy.Point(latitude=50.0965089, longitude=14.4082631)
r = geo_locator.reverse(test_point)

print(f"{r.raw['address']['road']}")
print(f"{r.raw['address']['suburb']}")
print(f"{r.raw['address']['city']}")
# 'address': {
#     'road': 'Badeniho',
#     'suburb': 'Holešovice',
#     'city': 'Hlavní město Praha',
