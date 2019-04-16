import pandas as pd

def get_csvs(station):
    df = pd.read_csv('dataframe.csv', index_col=0)
    df = df.loc[df['number'] == station]
    df.reset_index(drop=True)
    df.drop(['status', 'available_stands', 'description', 'week'], axis=1, inplace = True)
    df['Mean_Bikes'] = df.groupby(['time', 'day'])['available_bikes'].transform('mean').astype(int)
    df = df.drop_duplicates(subset=['day', 'time'], keep='last')
    df.reset_index(drop=True)
    df.drop(['available_bikes'], axis=1, inplace = True)
    path = 'graph_csvs/'
    df.to_csv(path + str(station)+'.csv')

df = pd.read_csv('dataframe.csv', index_col=0)
for i in df['number']:
    get_csvs(i)
