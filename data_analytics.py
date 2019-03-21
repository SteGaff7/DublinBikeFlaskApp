import pymysql
from pandas import DataFrame
import pandas as pd 
from datetime import datetime
import io 
import matplotlib.pyplot as plt

def get_data_analytics():
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
    
    df = DataFrame(get_data)
    df.columns = field_names
    
    df['last_update'] = pd.to_datetime(df.last_update, unit='ms')
    df['just_hour'] = df['last_update'].dt.hour
    df['just_date'] = df['last_update'].dt.date
    df['just_date'] = df['just_date'].astype('str')
    
    #here is where we will pass in name and date requested by user
    df = df.loc[(df['name'] == 'EXCHEQUER STREET') & (df['just_date'] == '2019-02-23')]
    df['available_bikes'].groupby([df['just_hour']]).mean().plot(kind='bar')

    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image
    

if __name__ == '__main__':
    pass