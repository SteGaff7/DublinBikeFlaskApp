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

        with urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=DUBLIN&apiKey=325a6c3fc2a812061a0adf4833eed7c5eb3b6813") as url:
            data = json.loads(url.read().decode())

        for i in range(0, len(data)):
            number = data[i]['number']
            name = data[i]['name']
            status = data[i]['status']
            bike_stands = data[i]['bike_stands']
            available_bike_stands = data[i]['available_bike_stands']
            available_bikes = data[i]['available_bikes']
            last_update = data[i]['last_update']
            banking = data[i]['banking']
            address = data[i]['address']
            lat = data[i]['position']['lat']
            lng = data[i]['position']['lng']


            cursor = connection.cursor()

            sql_insert_query = "REPLACE INTO `currentData` (`number`, `name`, `status`, `bike_stands`, `available_bikes`, `available_stands`, `last_update`, `banking`, `latitude`, `longitude`, `address`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            insert_tuple = (number, name, status, bike_stands, available_bikes, available_bike_stands, last_update, banking, lat, lng, address)

            result = cursor.execute(sql_insert_query, insert_tuple)
            connection.commit()

    except mysql.connector.Error as error :
        connection.rollback()
        #f=open('errorLog.txt','a')
        #f.write(error)
        #f.close()

    except Exception as error:
        pass
        #f=open('errorLog.txt','a')
        #f.write(error)
        #f.close()

    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

        time.sleep(40)