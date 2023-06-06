
import os
import pathlib
import time
import numpy as np

import pandas as pd

# mam sit bodu, ted projdu vsechny ctverce, tj zkontroluji jestli vsechny body jsou uvnitr Prahy
# nactene body beru jako sw roh

root_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), 'output')

square_distance = 1000

file_name_hdf = os.path.join(root_folder, f'grid_{str(square_distance).zfill(5)}.hdf')

df_points = pd.read_hdf(file_name_hdf)
max_ix = df_points['ix'].max()
max_iy = df_points['iy'].max()
state = 'praha'

# test ze ix. iy jsou unikatni (fakt by mely)
if len(np.unique(df_points[['ix', 'iy']], axis=0)) != len(df_points):
    print('INDEXY NEJSOU UNIKATNI!!')

if (max_ix+1) * (max_iy+1) != len(df_points):
    print('NESEDI POCET BODU!!')

for ix in range(0, max_ix+1):
    for iy in range(0, max_iy + 1):
        print (ix)
        print (iy)
        print ('----')
        # u sw rohu nemusim testovat, jestli je v df - urcite je
        sw_in = (df_points[(df_points['ix'] == ix) & (df_points['iy'] == iy)]['state'].iloc[0].lower() == 'state')

        # se
        if ix+1 <= max_ix:
            se_in = (df_points[(df_points['ix'] == ix+1) & (df_points['iy'] == iy)]['state'].iloc[0].lower() == 'state')
        else:
            se_in = False # ani neni v dataframe

        xxx = 0

