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
    #print(query)
    #print(result)
    return data

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