import time 
from flask import Flask, render_template, jsonify
import pymysql
import urllib.request
import json
import datetime
#Not needed below
import random

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

@app.route('/weatherToday')
def weatherToday():
    weather_array = []
    
    #Current Weather this instant
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

@app.route('/predictive_data/<details>')
def predictive(details):
    details_array = details.split('_')
    date = details_array[0]
    time = details_array[1]
    station_number = details_array[2]
    
    #Create a date object to calculate the weekday
    date_2 = date.replace('-', ' ', 2)
    date_object = datetime.datetime.strptime(date_2, '%Y %m %d')
    weekday = date_object.weekday()
    #print(date)
    #print(date_object)
    #print(weekday)
    
    #Round the time required for the prediction to the closest weather forecast time
    #Address 00:00 at some stage
    if time < '08:00' :
        rounded_time = '06:00:00'
    elif time < '11:00' :
        rounded_time = '09:00:00'
    elif time < '14:00' :
        rounded_time = '12:00:00'
    elif time < '17:00' :
        rounded_time = '15:00:00'
    elif time < '20:00' :
        rounded_time = '18:00:00'
    else:
        rounded_time = '21:00:00'
        
    #print(details_array, date, time, rounded_time, station_number)
    #date variable
     
    with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=0927fd5dff272fdbd486187e54283310") as url:
        data = json.loads(url.read().decode())

        weather_description_array = []
        weather_dict ={}
        for i in range(0, len(data["list"]), +1):
            #print(date,"GAP", data["list"][i]["dt_txt"])
            forecast_date_time = data["list"][i]["dt_txt"]
            forecast_date = forecast_date_time.split()[0]
            #print(forecast_date)
            
            #Only using weather forecast data for the day that we are interested in
            if date == forecast_date:              
                #Get the time for each forecast
                forecast_time = forecast_date_time.split()[1] 
                
                #Gather the weather description for the time slots that will appear on the graph
                if forecast_time in ['06:00:00','09:00:00','12:00:00','15:00:00','18:00:00','21:00:00']:
                    weather_description = data["list"][i]["weather"][0]["description"]
                    print(forecast_time, weather_description)
                    weather_description_array.append(weather_description)
                
                #Get the weather_description for the exact time specified
                if forecast_time == rounded_time:
                    specified_weather_description = data["list"][i]["weather"][0]["description"]
                    print(specified_weather_description)
                    
                #Get the weather for the slots that will be shown as part of the weather forecast
                if forecast_time == '09:00:00' or forecast_time == '12:00:00' or forecast_time == '15:00:00' or forecast_time == '18:00:00':
                    print(forecast_time)
                    icon = data["list"][i]["weather"][0]["icon"]
                    weather = data["list"][i]["weather"][0]["main"]
                    temp = str(round(int(data["list"][i]["main"]["temp"])-273.15)) + "°C"
                    print(weather, temp, icon)
                    
                    weather_dict[forecast_time] = {"weather" : weather, "temp" : temp, "icon" : icon}
        
        print(weather_description_array)
        
        #List of weather descriptions to use for the predictive data for the graph
        weather_description_for_graph = [None]*20
        
        #06:00
        for i in range(3):
            weather_description_for_graph[i] = weather_description_array[0]
        #09:00
        for i in range(3,6,+1):
            weather_description_for_graph[i] = weather_description_array[1]
        #12:00
        for i in range(6,9,+1):
            weather_description_for_graph[i] = weather_description_array[2]
        #15:00
        for i in range(9,12,+1):
            weather_description_for_graph[i] = weather_description_array[3]
        #18:00
        for i in range(12,15,+1):
            weather_description_for_graph[i] = weather_description_array[4]
        #21:00 +
        for i in range(15,20,+1):
            weather_description_for_graph[i] = weather_description_array[5]
        
        print(weather_description_for_graph)
            
        for i in weather_dict:
            print(i,weather_dict[i])
    
    #store weather for specified date and time
    
    #call predicitve data algorithm 
    
    #add all this info to an array to return
    
    time_array = ['0500','0600','0700','0800','0900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2000','2100','2200','2300','0000']
    
    
    graph_data_array = [0]*20
    
    print(str(station_number)+"_"+str(weekday)+".sav")
    #model = pickle.load(open(model/pickle/str(station_number)+"_"+str(weekday)+".sav"))
    
    
    #algo, for weather_description in weather_description_for_graph, run algo with weather, station number, the times from 0500 to 0000 and the date specified
    for i in range(0, len(weather_description_for_graph), +1):
        #dummy_algo(station_number, date, time_array[i], weather_description_for_graph[i])
        print("stat num", station_number, "weekday", weekday, "time", time_array[i], "weather description", weather_description_for_graph[i])
        y = random.randint(1,30)
        graph_data_array[i] = y
    
    #model(specified_weather_description, time)
    #algo for specified time, send in station number, time, date and weather description for specified time
    #dummy_algo(station_number, date, time, specified_weather_description)
    print("SPECIFIC")
    print("stat num",station_number, "weekday", weekday, "time", time.replace(":", ""), "weather description", specified_weather_description)
    specified_bikes_value = 10
    
    print(graph_data_array)
    print(weather_dict)
    print(specified_bikes_value)

    returning_data = [weather_dict, graph_data_array, specified_bikes_value]
    print(returning_data)
    return jsonify(returning_data)
    
    
    
    
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
def how_it_works():
    return render_template('how_it_works.html', title='About') # This points to the html page

@app.route("/subscription") # Tells the browser where to look
def subscription():
    return render_template('subscription.html', title='Subscriptions') # This points to the html page

@app.route("/contact") # Tells the browser where to look
def contact():
    return render_template('contact.html', title='Contact') # This points to the html page

if __name__ == '__main__': # This will allow us to run the and change the page without restarting the server
    app.run(debug=True)
