from flask import Flask, request, render_template, jsonify
import pymysql
from config import password

db = pymysql.connect("localhost", "root", f"{password}", "diabetes_db")

app = Flask(__name__)

@app.route('/')
def intro():
    return (
        f"Welcome to the diabetes app!<br/><br/>"
        f"Let's explore trends for adult diabetes and childhood obesity in different USA states in 2012 and in 2014.<br/><br/>"
        f"Available routes:<br/>"
        f"/data"
        )


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