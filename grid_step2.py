
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


file_namereduced_hdf = os.path.join(root_folder, f'grid_reduced_{str(square_distance).zfill(5)}.hdf')
file_namereduced_csv = os.path.join(root_folder, f'grid_reduced_{str(square_distance).zfill(5)}.csv')

df_points = pd.read_hdf(file_name_hdf)
# kopie kterou budu prepisovat
df_points_reduced  = df_points.copy()

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
        # u sw rohu nemusim testovat, jestli je v df - urcite je
        sw_in = (df_points[(df_points['ix'] == ix) & (df_points['iy'] == iy)]['state'].iloc[0].lower() == state)

        # se
        if ix+1 <= max_ix:
            se_in = (df_points[(df_points['ix'] == ix+1) & (df_points['iy'] == iy)]['state'].iloc[0].lower() == state)
        else:
            se_in = False # ani neni v dataframe

        if iy + 1 <= max_iy:
            nw_in = (df_points[(df_points['ix'] == ix) & (df_points['iy'] == iy+1)]['state'].iloc[0].lower() == state)
        else:
            nw_in = False  # ani neni v dataframe

        if (iy + 1 <= max_iy) and (ix+1 <= max_ix):
            ne_in = (df_points[(df_points['ix'] == ix+1) & (df_points['iy'] == iy+1)]['state'].iloc[0].lower() == state)
        else:
            ne_in = False  # ani neni v dataframe

        all_in = sw_in and se_in and nw_in and ne_in

        if not all_in:
            ix_replace = df_points_reduced[(df_points_reduced['ix'] == ix) & (df_points_reduced['iy'] == iy)].index
            df_points_reduced.loc[ix_replace, 'state'] = 'smazano'
        else:
            rrr = 0
            # nic

df_points_reduced.reset_index(inplace=True, drop=True)
df_points_reduced.to_csv(file_namereduced_csv)
df_points_reduced.to_hdf(file_namereduced_hdf, key='data')

praha_orig = len(df_points[df_points['state'].str.lower() == state])
praha_reduced = len(df_points_reduced[df_points_reduced['state'].str.lower() == state])

print(f'zredukovano z {praha_orig} na {praha_reduced}')
print('konec')







