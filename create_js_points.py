import os
import pathlib
import time
import numpy as np

import pandas as pd

# jen prepisu body do dict

root_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), 'output')

square_distance = 1000

file_name_hdf = os.path.join(root_folder, f'grid_{str(square_distance).zfill(5)}.hdf')
file_name_dict = os.path.join(root_folder, f'dict_{str(square_distance).zfill(5)}.json')

df_points = pd.read_hdf(file_name_hdf)
max_ix = df_points['ix'].max()
max_iy = df_points['iy'].max()
state = 'praha'

d = {}
id = 0

# test ze ix. iy jsou unikatni (fakt by mely)
if len(np.unique(df_points[['ix', 'iy']], axis=0)) != len(df_points):
    print('INDEXY NEJSOU UNIKATNI!!')

if (max_ix+1) * (max_iy+1) != len(df_points):
    print('NESEDI POCET BODU!!')

for ix in range(0, max_ix+1):
    for iy in range(0, max_iy + 1):
        one_point = df_points[(df_points['ix']==ix) & (df_points['iy']==iy)]

        if one_point['state'].iloc[0].lower() == 'praha':
            d[id] = f"{one_point['latitude'].iloc[0]}N,{one_point['longitude'].iloc[0]}E"
            id = id + 1

with open(file_name_dict, 'w') as f:
    f.write(str(d))