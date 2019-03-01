import mysql.connector
from flask import Flask, render_template, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__, static_url_path='')

engine = create_engine("mysql+mysqldb://ssk:villagebikes@villagebikesdb.c2v2pmaab8cg.us-east-2.rds.amazonaws.com:3306/VillageBikesDB")
connection = engine.connect()
result = connection.execute("select * from staticData")
data = result.fetchall()
for row in data:
    print(row)
print(type(data))
connection.close


@app.route("/")
@app.route("/home")
def home():
    #posts in template is equal to post here
    return render_template('home.html')

@app.route("/testStatic")
def test():
    return render_template("test.html", data=data)
    
@app.route("/about")
def about():
    return render_template('about.html')
'''
def connect_to_database():
    engine = create_engine("mysql+mysqldb://ssk:villagebikes@villagebikesdb.c2v2pmaab8cg.us-east-2.rds.amazonaws.com:3306/VillageBikesDB")
    connection = engine.connect()
    print(engine)
    return connection



@app.route("/test")
def test():
    connection = connect_to_database()
    result = connection.execute("select * from staticData")
    for row in result:
        print(row)
    return result
  '''  
    
'''
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.route("/stations")
def get_stations():
    engine = get_db()
    stations = []
    rows = engine.execute("SELECT * from staticData;")
    for row in rows:
        stations.append(dict(row))
    
    return jsonify(stations=stations)
 '''
 
if __name__ == "__main__":
    app.run(debug=True)
    
