import pandas as pd
df1 = 0
df2 = 0

if False:
    data1 = [10, 20, 30, 40, 50, 60]
    df1 = pd.DataFrame(data1, columns=['Numbers'])

    data2 = [100, 200, 300, 400, 500, 600]
    df2 = pd.DataFrame(data2, columns=['cisla'])



    df1.to_hdf('soubor.h5', key='d1')
    df2.to_hdf('soubor.h5', key='d2')

df1 = pd.read_hdf('soubor.h5', key='d1')
df2 = pd.read_hdf('soubor.h5', key='d2')

print(df1)
print(df2)