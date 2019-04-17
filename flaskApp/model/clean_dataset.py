import pandas as pd

def clean_data():
    df = pd.read_csv('full_dataframe.csv', index_col=0)

    for col in df[['description']].columns:
        if [df['description']=='clear sky']:
            df['description'].replace('clear sky',1, inplace=True)
        if[df['description']=='few clouds']:
            df['description'].replace('few clouds', 2, inplace=True)
        if[df['description']=='scattered clouds']:
            df['description'].replace('scattered clouds',3, inplace=True)
        if [df['description']=='broken clouds']:
            df['description'].replace('broken clouds',4, inplace=True)
        if [df['description']=='fog']:
            df['description'].replace('fog',5, inplace=True)
        if [df['description']=='mist']:
            df['description'].replace('mist',6, inplace=True)
        if [df['description']=='light intensity drizzle']:
            df['description'].replace('light intensity drizzle',7, inplace=True)
        if [df['description']=='light intensity drizzle rain']:
            df['description'].replace('light intensity drizzle rain',8, inplace=True)
        if [df['description']=='light intensity shower rain']:
            df['description'].replace('light intensity shower rain',9, inplace=True)
        if [df['description']=='shower rain']:
            df['description'].replace('shower rain',10, inplace=True)
        if [df['description']=='heavy intensity rain']:
            df['description'].replace('heavy intensity rain',11, inplace=True)
        if [df['description']=='light rain']:
            df['description'].replace('light rain',12, inplace=True)
        if [df['description']=='moderate rain']:
            df['description'].replace('moderate rain',13, inplace=True)
        if [df['description']=='very heavy rain']:
            df['description'].replace('very heavy rain',14, inplace=True)
        if [df['description']=='shower sleet']:
            df['description'].replace('shower sleet',15, inplace=True)
        if [df['description']=='snow']:
            df['description'].replace('snow',16, inplace=True)
        if [df['description']=='overcast clouds']:
            df['description'].replace('overcast clouds',17, inplace=True)


    df['last_update'] = df['last_update'].astype('datetime64[ns]')
    df['week'] = df['last_update'].dt.week
    df['day'] = df['last_update'].dt.weekday
    df['last_update'] = df['last_update'].dt.round('30min')
    df['time'] =df.last_update.map(lambda t: t.strftime('%H%M'))
    df = df.drop_duplicates()
    df = df.drop(['last_update', 'banking', 'bike_stands', 'weather_id', 'main', 'temperature', 'humidity', 'wind_speed'] , axis=1)

    df.to_csv('dataframe.csv')

clean_data()
