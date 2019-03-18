import time 
from flask import Flask, render_template, jsonify
import pymysql
import urllib.request
import json
from mysql.connector.errorcode import CR_INSECURE_API_ERR

app = Flask(__name__, static_url_path='')

def connect_to_database():
   host = 'villagebikesdb.c2v2pmaab8cg.us-east-2.rds.amazonaws.com'
   port=3306
   dbname = 'VillageBikesDB'
   user='ssk'
   password='villagebikes'

   connection = pymysql.connect(host, user=user, passwd=password, db=dbname)
   return connection


#Establish connection and assign to connection
connection = connect_to_database()

@app.route("/home") # Tells the browser where to look
def home():
    try:    
        with connection.cursor() as cursor:
                sql = 'SELECT * FROM currentData'
                cursor.execute(sql)
                currentData = cursor.fetchall()
            
    except:
       print('Error')

    return render_template("home.html", Data=currentData)

@app.route('/retrieve/<stationNumber>')
def retrieve(stationNumber):
    
    query = "select available_bikes, available_stands, last_update from currentData where number="+str(stationNumber)
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
        result = cursor.fetchall()
    data = jsonify(result)
    print(query)
    print(result)
    return data

'''
@app.route('/retrieve/<stationNumber>')
def retrieve(stationNumber):
    query = "select available_bikes, available_stands, last_update from currentData where number="+str(stationNumber)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    data = jsonify(result)
    print(query)
    print(result)
    return data
'''

@app.route("/about") # Tells the browser where to look
def How_it_works():
    return render_template('how_it_works.html', title='About') # This points to the html page

@app.route("/subscription") # Tells the browser where to look
def subscription():
    return render_template('subscription.html', title='Subscriptions') # This points to the html page

@app.route("/contact") # Tells the browser where to look
def Contact():
    return render_template('contact.html', title='Contact') # This points to the html page

if __name__ == '__main__': # This will allow us to run the and change the page without restarting the server
    app.run(debug=True)
    

#OLD FUNCTIONS

#query = "select number, name, available_bikes, available_stands, last_update from dynamicData D1 where last_update = (select max(last_update) from dynamicData D2 where D1.number = D2.number)"

'''
@app.route('/retrieve/<stationNumber>')
def retrieve(stationNumber):
    query = "select max(last_update), number, name, available_bikes, available_stands from dynamicData where number="+str(stationNumber)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    data = jsonify(result)
    return data
'''


'''
@app.route("/home") # Tells the browser where to look
def home():
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM staticData'
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    except:
        print('Error')
        
    return render_template("home.html", data=result)
'''

'''   
@app.route("/home2") # Tells the browser where to look
def home():
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM staticData'
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    except:
        print('Error')
    
    try: 
        with urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=DUBLIN&apiKey=325a6c3fc2a812061a0adf4833eed7c5eb3b6813") as url:
            data2 = json.loads(url.read().decode())
    
    except:
        print("Error with scrape")
    
    dynamic_array = []
    
    for i in range(0, len(data2)):
        number = data2[i]['number']
        name = data2[i]['name']
        status = data2[i]['status']
        #bike_stands = data2[i]['bike_stands']
        available_bike_stands = data2[i]['available_bike_stands']
        available_bikes = data2[i]['available_bikes']
        last_update = data2[i]['last_update']
        #banking = data2[i]['banking']
        dynamic_array += [number,name,status,available_bikes,available_bike_stands, last_update]
        
    print(data2)
    #except:
        #print("Dynamic Error")
    
    return render_template("home2.html", data=result, dynamicData=data2)


@app.route("/home") # Tells the browser where to look
def home():
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM staticData'
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    except:
        print('Error')
        
    return render_template("home.html", data=result)
'''