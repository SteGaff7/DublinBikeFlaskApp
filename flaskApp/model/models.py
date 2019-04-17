# Library Imports.
import pandas as pd
import numpy as np
from patsy import dmatrices
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_predict, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.tree import export_graphviz
import pydot
import pickle
import math

def find_bikes(station, day):
    df = pd.read_csv('dataframe.csv', index_col=0)
    df = df.loc[(df['day'] == day) & (df['number'] == station)]
    df['time'] = df['time'].astype('int64')
    df.reset_index(drop=True)

    item_list = list(range(df.shape[1]))
    #???
    list_to_remove = [0,1,2,3,4,6,7]
    final_list= list(set(item_list).difference(set(list_to_remove)))

    X = df.iloc[:, final_list].values
    y = df.iloc[:, 3].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=False)
    model = RandomForestRegressor(n_estimators=1000, random_state=0)
    model.fit(X_train, y_train)

    pickle_model = 'pickles/' + str(station)+'_'+ str(day)+'.sav'
    pickle.dump(model, open(pickle_model, 'wb'))


    return pickle_model

df = pd.read_csv('dataframe.csv', index_col=0)

for i in df['number']:
    for j in range(7):
        find_bikes(i, j)
