import mysql.connector, time
from flask import Flask, render_template, g, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from mysql.connector.errorcode import CR_INSECURE_API_ERR
import pymysql

app = Flask(__name__, static_url_path='')


def connect_database():
    host = 'villagebikesdb.c2v2pmaab8cg.us-east-2.rds.amazonaws.com'
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
except:
    print("Hello")

#Root route
@app.route("/")
#Home Page
@app.route("/home")
def home():
    return render_template('home.html')

#About Page
@app.route("/about")
def about():
    return render_template('about.html')

#Static Map page
@app.route("/static")
def test():

        # Read a single record
        # result = connection.execute("select * from staticData")
        # data = result.fetchall()
        # print(type(result))
        # print(data)
        # print(data[0])
        return render_template("map.html", data=result)

@app.route("/dynamic")
# def testDynamic():
#     #Current timestamp in ms
#     current_time = time.time()*1000
#     #print(current_time)
#     #print(str(current_time-300000))
#     query = "select number, name, available_bikes from dynamicData where `last_update`>"+str(current_time-300000)
#     result = connection.execute(query)
#     data = result.fetchall()
#     print(type(result))
#     #for row in data:
#     #    print(row)
#     #    print(type(row))
#     return render_template("dynamicData.html", data=data)

#Get Test Script
# @app.route("/testStatic2", methods=['GET', 'POST'])
# def test2():
#     result = connection.execute("select * from staticData")
#     data = result.fetchall()
#     print(type(result))
#     return render_template("anothertest.html", data=data)

#Test Script
@app.route('/_add_numbers')
# def add_numbers():
#     a = request.args.get('a', 0, type=int)
#     b = request.args.get('b', 0, type=int)
#     return jsonify(result=a + b)

#Test Script
@app.route('/index2')
def index():
    return render_template('index2.html')

if __name__ == "__main__":
    app.run(debug=True)



'''
#Old routes

@app.route("/loadtest")
def loadtest():
    return render_template('loadtest.html')

@app.route("/map")
def maps():
    return render_template('map2.html')

result = connection.execute("select * from staticData")
data = result.fetchall()
for row in data:
    print(row)
print(type(data))
connection.close

'''
