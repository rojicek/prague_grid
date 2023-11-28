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
    for i
    return True


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
            i = check_inside(one_point, squares_df)

            x = 0



sss = 0