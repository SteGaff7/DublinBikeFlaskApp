import pymysql
from pandas import DataFrame
import pandas as pd 

host   = 'villagebikesdb.c2v2pmaab8cg.us-east-2.rds.amazonaws.com'
port   = 3306
user   = 'ssk'
passwd = 'villagebikes'
db     = 'VillageBikesDB'

cnx    = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
cur    = cnx.cursor()

query  = """SELECT * FROM weatherData"""
cur.execute(query)

field_names = [i[0] for i in cur.description]
get_data = [xx for xx in cur]

cur.close()
cnx.close()

df1 = DataFrame(get_data)
df1.columns = field_names
df1['timestamp'] = pd.to_datetime(df1.timestamp,unit='s')
df1 = df1.rename(index=str, columns={"timestamp": "last_update"})

host   = 'villagebikesdb.c2v2pmaab8cg.us-east-2.rds.amazonaws.com'
port   = 3306
user   = 'ssk'
passwd = 'villagebikes'
db     = 'VillageBikesDB'

cnx    = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
cur    = cnx.cursor()

query  = """SELECT * FROM dynamicData"""
cur.execute(query)

field_names = [i[0] for i in cur.description]
get_data = [xx for xx in cur]

cur.close()
cnx.close()

df2 = DataFrame(get_data)
df2.columns = field_names
df2['last_update'] = pd.to_datetime(df2.last_update,unit='ms')


df1 = df1.sort_values(by=['last_update'])
df2 = df2.sort_values(by=['last_update'])


df3 = pd.merge_asof(df2,df1, on='last_update', direction='nearest')
df3['last_update'] = pd.to_datetime(df3.last_update, unit='ms')
df3.to_csv('full_dataframe.csv')












