import time 
from flask import Flask, render_template
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
