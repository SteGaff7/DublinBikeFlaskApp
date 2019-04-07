import time 
from flask import Flask, render_template, jsonify
import pymysql
import urllib.request
import json
#Not needed below
import random
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
    #print(query)
    #print(result)
    return data

@app.route('/algo/<stuff>')
def predictive(stuff):
    #stuff = jsonify(stuff)
    return jsonify(stuff)

@app.route('/weatherToday')
def weatherToday():
    weather_array = []
    
    #Current Weather
    with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=0927fd5dff272fdbd486187e54283310") as url:
        data = json.loads(url.read().decode())
        
        weather = data["weather"][0]["main"]
        icon = data["weather"][0]["icon"]
        temp = str(round(int(data["main"]["temp"])-273.15)) + "°C"
        
        weather_array = [["Now", weather, temp, icon],[],[],[]]
    
    #Next 3 weather forecasts
    with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=0927fd5dff272fdbd486187e54283310") as url:
        data = json.loads(url.read().decode())
        
        for i in range(1, 4, +1):
            print(data["list"][i]["dt_txt"])
            forecast_date_time = data["list"][i]["dt_txt"]
            forecast_date = forecast_date_time.split()[0]
            forecast_time = forecast_date_time.split()[1]
            forecast_time_slice = forecast_time[0:5]
            
            print(forecast_time)
            icon = data["list"][i]["weather"][0]["icon"]
            weather = data["list"][i]["weather"][0]["main"]
            temp = str(round(int(data["list"][i]["main"]["temp"])-273.15)) + "°C"
            print(weather, temp, icon)
            
            weather_array[i] = [forecast_time_slice, weather, temp, icon]

        
    #for i in weather_dict:
     #   print(i,weather_dict[i])
    
    return jsonify(weather_array)        
    #return jsonify(weather_dict)

@app.route('/weatherForecast/<date>')
def weatherForecast(date):
    with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=0927fd5dff272fdbd486187e54283310") as url:
        data = json.loads(url.read().decode())
        weather_dict ={}
        for i in range(0, len(data["list"]), +1):
            print(date,"GAP", data["list"][i]["dt_txt"])
            forecast_date_time = data["list"][i]["dt_txt"]
            forecast_date = forecast_date_time.split()[0]
            print(forecast_date)
            if date == forecast_date:
                forecast_time = forecast_date_time.split()[1] 
                print(forecast_time)
                
                if forecast_time == '09:00:00' or forecast_time == '12:00:00' or forecast_time == '15:00:00' or forecast_time == '18:00:00':
                    print(forecast_time)
                    icon = data["list"][i]["weather"][0]["icon"]
                    weather = data["list"][i]["weather"][0]["main"]
                    temp = str(round(int(data["list"][i]["main"]["temp"])-273.15)) + "°C"
                    print(weather, temp, icon)
                    
                    weather_dict[forecast_time] = {"weather" : weather, "temp" : temp, "icon" : icon}
                    
            print()     
            
        for i in weather_dict:
            print(i,weather_dict[i])   

    return jsonify(weather_dict)


@app.route("/chart_data")
def get_chart_data():
    random_array = []
    for x in range(20):
        y = random.randint(1,41)
        print(y)
        random_array += [y]
    return jsonify(random_array)

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
