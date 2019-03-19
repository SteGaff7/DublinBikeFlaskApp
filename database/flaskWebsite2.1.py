from flask import Flask, render_template
import pymysql
import pandas as pd
#import pymysql.cursor
app = Flask(__name__)

def connect_database():
    host = "villagebikesdb.c2v2pmaab8cg.us-east-2.rds.amazonaws.com"
    port=3306
    dbname = "VillageBikesDB"
    user="ssk"
    password="villagebikes"

    connection = pymysql.connect(host, user=user,
    passwd=password, db=dbname)

    return connection

connection = connect_database()

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM staticData"
        cursor.execute(sql)
        result = cursor.fetchall()
        # staticdb = pd.read_sql_query(sql, connection)
        # print(staticdb)
        for i in result:
            print(i[1], i[3], i[4])
        # print(type(result))

# https://gist.github.com/simonbingham/2652757

@app.route("/home") # Tells the browser where to look
def home():
    return render_template('home.html') # This points to the html page

@app.route("/about") # Tells the browser where to look
def How_it_works():
    return render_template('about.html', title='About') # This points to the html page

@app.route("/subscription") # Tells the browser where to look
def subscription():
    return render_template('subscription.html', title='Subscriptions') # This points to the html page

@app.route("/contact") # Tells the browser where to look
def Contact():
    return render_template('contact.html', title='Contact') # This points to the html page


if __name__ == '__main__': # This will allow us to run the and change the page without restarting the server
    app.run(debug=True)

"""
Put in a 'static folder'
Put in a 'error page'
"""
