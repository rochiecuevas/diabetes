from flask import Flask, request, render_template, jsonify
import pymysql
from config import password

db = pymysql.connect("localhost", "root", f"{password}", "diabetes_db")

app = Flask(__name__)

@app.route('/')
def index():
    cursor = db.cursor()
    sql = "SELECT * FROM merged"
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description] # gets the column headers in the merged table
    results = [dict(zip(columns, row)) for row in cursor.fetchall()] # output is a list of dictionaries
    return render_template("index.html", results = results)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)