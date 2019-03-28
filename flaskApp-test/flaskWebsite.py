import time
from flask import Flask, render_template, flash, request
import pymysql

app = Flask(__name__, static_url_path='')

def connect_to_database():
   host = 'villagebikesdb.c2v2pmaab8cg.us-east-2.rds.amazonaws.com'
   port=3306
   dbname = 'VillageBikesDB'
   user='ssk'
   password='villagebikes'

   connection = pymysql.connect(host, user=user, passwd=password, db=dbname)
   return connection

connection = connect_to_database()

#Establish connection and assign to connection
connection = connect_to_database()

def get_user_station_info(address, date, time, station):

    f= open("print.txt","w")

    f.write("This is the the address: " + address + "\n")
    f.write("This is the the address: " + date + "\n")
    f.write("This is the the address: " + time + "\n")
    f.write("This is the preference: " + station + "\n")

    return("Okay")

@app.route("/home", methods=["POST", "GET"]) # Tells the browser where to look
def home():
    if request.method == "POST":

        try:
            with connection.cursor() as cursor:
                sql = 'SELECT * FROM staticData'
                cursor.execute(sql)
                result = cursor.fetchall()
        except:
            print('Error')

        address = request.form['address']
        date = request.form['date']
        time = request.form['time']
        station = request.form['station']

        get_user_station_info(address, date, time, station)

        result_2 = (address, date, time, station)

        return render_template("home.html", data=result, box=result_2)
    else:
        try:
            with connection.cursor() as cursor:
                sql = 'SELECT * FROM staticData'
                cursor.execute(sql)
                result = cursor.fetchall()
        except:
            print('Error')

        return render_template("home.html", data=result)

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
