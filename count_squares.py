# klicovy krok
# nacte postupne vsechny gpx a kazdy bod z nich zkontroluje proti gridu
# uklada si vlastni 'cache': already_processed_gpx ve kterem ma uz zpracovane

import os
import pandas as pd


work_folder = r'c:\Users\jiri\Documents\dev_code\Prague_grid\prague_grid\output'
base_file = 'grid_03000.hdf'
squares_file = 'squares_03000.hdf'
rides_folder = r'c:\Users\jiri\Documents\dev_code\Prague_grid\prague_grid\rides\processed_activities_df'


def check_inside(point, grid):
    for sw_point_index in range(len(grid)):
        # chapu jako jihozapadni roh (min lan, min lot)
        ix = grid.loc[sw_point_index, 'ix']
        iy = grid.loc[sw_point_index, 'iy']

        sw_point = grid[(grid['ix'] == ix + 0) & (grid['iy'] == iy + 0)]
        se_point = grid[(grid['ix'] == ix + 1) & (grid['iy'] == iy + 0)]
        ne_point = grid[(grid['ix'] == ix + 1) & (grid['iy'] == iy + 1)]
        nw_point = grid[(grid['ix'] == ix + 0) & (grid['iy'] == iy + 1)]

        all_ok = True

        all_ok = all_ok and (sw_point['state'].values[0].lower() == 'praha')
        all_ok = all_ok and (se_point['state'].values[0].lower() == 'praha')
        all_ok = all_ok and (ne_point['state'].values[0].lower() == 'praha')
        all_ok = all_ok and (nw_point['state'].values[0].lower() == 'praha')

        # tohle neni uplne presne, protoze to nemusi byt ctverek podel souradnic
        min_latitude = min(sw_point['latitude'].values[0], se_point['latitude'].values[0])
        max_latitude = min(nw_point['latitude'].values[0], ne_point['latitude'].values[0])

        min_longitude = min(sw_point['longitude'].values[0], nw_point['longitude'].values[0])
        max_longitude = min(se_point['longitude'].values[0], ne_point['longitude'].values[0])

        if min_latitude <= point.latitude <= max_latitude and min_longitude <= point.longitude <= max_longitude:
            return True
        else:
            return False



# try to open squares_file
squares_full_filename = os.path.join(work_folder, squares_file)
if os.path.isfile(squares_full_filename):
    squares_df = pd.DataFrame(pd.read_hdf(squares_full_filename, key='grid'))
    processed_gpx_df = pd.DataFrame(pd.read_hdf(squares_full_filename, key='gpx'))
else:
    # neexistuji zadne vysledky, zalozim prazdne df podle base gridu
    squares_df = pd.DataFrame(pd.read_hdf(os.path.join(work_folder, base_file)))
    squares_df['gpx_file'] = ''
    squares_df['been_there'] = 0  # nikde jsem nebyl
    processed_gpx_df = pd.DataFrame(columns=['gpx_file', 'squares_covered'])

    squares_df.to_hdf(squares_full_filename, key='grid')
    processed_gpx_df.to_hdf(squares_full_filename, key='gpx')

# loop over rides
for foldername, subfolders, filenames in os.walk(rides_folder):
    # Print information about each file in the current folder
    for filename in filenames:
        ride_file_path = os.path.join(foldername, filename)
        print('Processing ride:', ride_file_path)

        ride_df = pd.DataFrame(pd.read_hdf(ride_file_path))
        for index, one_point in ride_df.iterrows():
            point_in = check_inside(one_point, squares_df)

            x = 0



sss = 0