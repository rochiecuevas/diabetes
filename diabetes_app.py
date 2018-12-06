from flask import Flask, request, render_template, jsonify
import pymysql
from config import password

db = pymysql.connect("localhost", "root", f"{password}", "diabetes_db")

app = Flask(__name__)

@app.route('/')
def intro():
    return render_template("index.html")

@app.route('/states&obesity2012')
def obesity2012():
    return render_template("states_obesity_2012.html")

@app.route('/states&obesity2014')
def obesity2014():
    return render_template("states_obesity_2014.html")

@app.route('/states&diabetes2012')
def diabetes2012():
    return render_template("states_diabetes_2012.html")

@app.route('/states&diabetes2014')
def diabetes2014():
    return render_template("states_diabetes_2014.html")

@app.route('/diabetes2012&2014')
def obdia2012():
    return render_template("diabetics_2012_2014.html")

@app.route('/obesity2012&2014')
def obdia2014():
    return render_template("obesity_2012_2014.html")

@app.route('/data')
def index():
    cursor = db.cursor()
    sql = "SELECT * FROM merged"
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description] # gets the column headers in the merged table
    results = [dict(zip(columns, row)) for row in cursor.fetchall()] # output is a list of dictionaries
    return render_template("data.html", results = results)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)