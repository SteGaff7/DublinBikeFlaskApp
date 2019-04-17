#! /usr/bin/python3

import urllib.request, json, mysql.connector, time
from mysql.connector import Error
from mysql.connector import errorcode

while True:

    try:
        connection = mysql.connector.connect(host='villagebikesdb.c2v2pmaab8cg.us-east-2.rds.amazonaws.com',
                                             port='3306',
                                             database='VillageBikesDB',
                                             user='ssk',
                                             password='villagebikes')
    
        with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=0927fd5dff272fdbd486187e54283310") as url:
            data = json.loads(url.read().decode())
    
            time_updated = data["dt"]
            weather_id = data["weather"][0]["id"]
            main = data["weather"][0]["main"]
            description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
    
        cursor = connection.cursor()
    
        sql_insert_query = "INSERT IGNORE INTO `weatherData` (`timestamp`, `weather_id`, `main`, `description`, `temperature`, `humidity`, `wind_speed`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    
        insert_tuple = (time_updated, weather_id, main, description, temp, humidity, wind_speed)
    
        result = cursor.execute(sql_insert_query, insert_tuple)
        connection.commit()
        #print("Inserted success")    

    except mysql.connector.Error as error :
        connection.rollback()
        #f=open('errorLogWeather.txt','a')
        #f.write(error)
        #f.close()  

    except Exception as error:
        f=open('errorLogWeather.txt','a')
        #f.write(error)
        f.close()

    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

            
        time.sleep(1200)
