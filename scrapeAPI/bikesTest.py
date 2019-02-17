#! /usr/bin/python3

import urllib.request, json, mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

def insertVariableInTable(number, name, banking, bike_stands, available_bike_stands, available_bikes):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='testDB',
                                             user='stephen',
                                             password='1993')
        
        cursor = connection.cursor()
        
        sql_insert_query = "INSERT INTO `test3` (`number`, `name`, `banking`, `bikeStands`, `availableStands`, `availableBikes`) VALUES (%s,%s,%s,%s,%s,%s)"
        
        insert_tuple = (number, name, banking, bike_stands, available_bike_stands, available_bikes)
        
        result = cursor.execute(sql_insert_query, insert_tuple)
        connection.commit()
        print("Inserted success")
        
    except mysql.connector.Error as error :
        connection.rollback()
        print("Failed inserting record into python_users table {}".format(error))  
    
    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            

with urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=DUBLIN&apiKey=325a6c3fc2a812061a0adf4833eed7c5eb3b6813") as url:
    data = json.loads(url.read().decode())
    
for i in range(1,20):
    number = data[i]['number']
    name = data[i]['name']
    banking = data[i]['banking']
    bike_stands = data[i]['bike_stands']
    available_bike_stands = data[i]['available_bike_stands']
    available_bikes = data[i]['available_bikes']
    
    insertVariableInTable(number, name, banking, bike_stands, available_bike_stands, available_bikes)
