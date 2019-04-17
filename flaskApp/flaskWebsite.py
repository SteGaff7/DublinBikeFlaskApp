import time 
from flask import Flask, render_template, jsonify
import pymysql
import urllib.request
import json
import datetime
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

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

@app.route("/")
def home():
    '''
    Home page will automatically query the most recent data from the SQL Db and load this into the home.html template
    '''
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
    '''
    Retrieve the most up to date data for a specified station number
    '''
    
    query = "select available_bikes, available_stands, last_update from currentData where number="+str(stationNumber)
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
        result = cursor.fetchall()
    data = jsonify(result)

    return data

@app.route('/weatherToday')
def weatherToday():
    weather_array = []
    '''
    Get weather forecast for right now and the next 3 forecasts for the day. Return this as a list with lists within
    '''
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
            #print(data["list"][i]["dt_txt"])
            forecast_date_time = data["list"][i]["dt_txt"]
            forecast_date = forecast_date_time.split()[0]
            forecast_time = forecast_date_time.split()[1]
            forecast_time_slice = forecast_time[0:5]
            
            icon = data["list"][i]["weather"][0]["icon"]
            weather = data["list"][i]["weather"][0]["main"]
            temp = str(round(int(data["list"][i]["main"]["temp"])-273.15)) + "°C"
            
            weather_array[i] = [forecast_time_slice, weather, temp, icon]
    
    return jsonify(weather_array)        

@app.route("/chart_data/<station_number>")
def get_chart_data(station_number):
    '''
    Get chart data for a specified station and day, stored in a csv file generated from a python script which uses pandas
    '''
    csv = "model/graph_csvs/"+str(station_number)+".csv"
    df = pd.read_csv(csv, index_col=0)
    
    #Get the current day as an int
    today = datetime.datetime.now().weekday()
    
    graph_data_list = []
    time_list = [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 0]
    for i in time_list:
        row = df[(df['day']==today) & (df['time'] == i)]
        mean_bikes = int(row.iloc[0]['Mean_Bikes'])
        graph_data_list.append(mean_bikes)
    
    return jsonify(graph_data_list)

@app.route('/predictive_data/<details>')
def predictive(details):
    '''
    Route used for returning the predictive data and weather forecast to the HTML page
    Returns an array that contains a weather dictionary for the weather forecast for that day, an array of predicted bike availability values for that day for use
    on the graph and an integer that represents the predicted number of bikes for the specified time.
    
    '''
    
    #Details received in form date_time_stationNumber
    details_array = details.split('_')
    date = details_array[0]
    time = details_array[1]
    station_number = details_array[2]
    
    #Create a date object to calculate the weekday
    date_2 = date.replace('-', ' ', 2)
    date_object = datetime.datetime.strptime(date_2, '%Y %m %d')
    weekday = date_object.weekday()
    
    #Round the time required for the prediction to the closest weather forecast time
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
        
    #Call the weather API
    with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=0927fd5dff272fdbd486187e54283310") as url:
        data = json.loads(url.read().decode())
        
        #Create and array for the weather descriptions for that day (to be used with the predictive graph)
        weather_description_array = []
        
        #Create a weather dictionary that will be used to store the weather forecast data (09:00, 12:00, 15:00, 18:00)
        weather_dict ={}
        for i in range(0, len(data["list"]), +1):
            
            #Get forecast date and time
            forecast_date_time = data["list"][i]["dt_txt"]
            forecast_date = forecast_date_time.split()[0]
            
            #Only using weather forecast data for the day that we are interested in
            if date == forecast_date:              
                #Get the time for each forecast
                forecast_time = forecast_date_time.split()[1] 
                
                #Gather the weather description for the time slots that will appear on the graph
                if forecast_time in ['06:00:00','09:00:00','12:00:00','15:00:00','18:00:00','21:00:00']:
                    weather_description = data["list"][i]["weather"][0]["description"]
                    #Append to weather description array
                    weather_description_array.append(weather_description)
                
                #Get the weather_description for the exact time specified
                if forecast_time == rounded_time:
                    specified_weather_description = data["list"][i]["weather"][0]["description"]
                    
                #Get the weather for the slots that will be shown as part of the weather forecast
                if forecast_time == '09:00:00' or forecast_time == '12:00:00' or forecast_time == '15:00:00' or forecast_time == '18:00:00':
                    #Store icon, weather and temperature for that time of the specified day in the weather dictionary 
                    icon = data["list"][i]["weather"][0]["icon"]
                    weather = data["list"][i]["weather"][0]["main"]
                    temp = str(round(int(data["list"][i]["main"]["temp"])-273.15)) + "°C"
                    #Store forecast in a dictionary with the time as the key and a sub-dict as the value
                    weather_dict[forecast_time] = {"weather" : weather, "temp" : temp, "icon" : icon}
        
        #Function to change a weather description to the code needed for the predictive model
        def change_weather_description(weather_description):
            weather_description_to_code_dict ={
                "clear sky" : 1,
                "few clouds" : 2,
                "scattered clouds" : 3,
                "broken clouds" : 4,
                "fog" : 5,
                "mist" : 6,
                "light intensity drizzle" : 7,
                "light intensity drizzle rain" : 8,
                "light intensity shower rain" : 9,
                "shower rain" : 10,
                "heavy intensity rain" : 11,
                "light rain" : 12,
                "moderate rain" : 13,
                "very heavy rain" : 14,
                "shower sleet" : 15,
                "snow" : 16,
                "overcast clouds" : 17
                }
            coded_weather_description = weather_description_to_code_dict[weather_description]
            return coded_weather_description
        
        #List of weather descriptions to use for the predictive data for the graph
        weather_description_for_graph = [None]*20
        
        #Allocate the closest weather description to a time slot, e.g, 05:00 match to 06:00 weather forecast description
        #06:00 e.g 05:00, 06:00, 07:00
        for i in range(3):
            weather_description_for_graph[i] = weather_description_array[0]
        #09:00 e.g 08:00, 09:00, 10:00
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

    #Get rid of the colon in the time variable
    time = time.replace(":", "")
    
    #Call function to change weather description to code
    specified_weather_description = change_weather_description(specified_weather_description)
    
    #Array of times that will display on the predictive graph
    time_array = ['0500','0600','0700','0800','0900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2000','2100','2200','2300','0000']
    
    #Empty list that will hold the predictive data of the amount of bikes for the corresponding time slot above
    graph_data_array = [0]*20
    
    file = open("model/pickles/"+str(station_number)+"_"+str(weekday)+".sav", "rb")
    #file = open("/home/stephen/Documents/College/Semester2/Eclipse_Workspace/SEProject/SEProject/flaskApp/model/pickles/"+str(station_number)+"_"+str(weekday)+".sav", "rb")
    model = pickle.load(file)
    
    #Call the model 20 times for times from 0500 to 2400 with the relevant weather description
    for i in range(0, len(weather_description_for_graph), +1):   
        #Convert weather description to code     
        w_description = change_weather_description(weather_description_for_graph[i])
        #print("Calling predictive model with following:", str(station_number)+"_"+str(weekday)+".sav, time:", str(time_array[i]), "weather description", weather_description_for_graph[i])
        #Predict the bike availability for this index of the time_array and weather_description_graph
        bike_prediction = int(model.predict([[str(time_array[i]), str(w_description)]]))
        #Change the value of the empty graph_data_array by index e.g index 0 =0500, index 1 =0600.. etc
        graph_data_array[i] = bike_prediction
    
    #print("Calling predictive model with following:", str(station_number)+"_"+str(weekday)+".sav, time:", time, "weather description", specified_weather_description)
    #Call the model for the specified time slot
    specified_bikes_value = model.predict([[str(time), str(specified_weather_description)]])
    
    #Convert class 'numpy.ndarray' to int
    specified_bikes_value = int(specified_bikes_value)    
    returning_data = [weather_dict, graph_data_array, specified_bikes_value]

    return jsonify(returning_data)


@app.route("/about")
def how_it_works():
    return render_template('how_it_works.html', title='About')

@app.route("/subscription")
def subscription():
    return render_template('subscription.html', title='Subscriptions')

@app.route("/contact") # Tells the browser where to look
def contact():
    return render_template('contact.html', title='Contact')

if __name__ == '__main__': # This will allow us to run the and change the page without restarting the server
    app.run(debug=True)
