from flask import Flask, g, render_template, abort, request
import json
import pyodbc
import folium
import pandas as pd
import requests
import time
# import MIS5440Project.MapLists as ml


###############
# CREATE APIs #
###############

# Create connection
connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:mis5400schooldata.database.windows.net,1433;Database=school_rankings;Uid=elsagreenwalt;\
                    Pwd=Mis5400fa2019;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Set up Flask
app = Flask(__name__)
app.config.from_object(__name__)

# Make sure we are connected to the database
@app.before_request
def before_request():
    try:
        g.sql_conn = pyodbc.connect(connection_string, autocommit=True)
    except Exception:
        abort(500, "No database connection could be established.")

# Tear down request
@app.teardown_request
def teardown_request(exception):
    try:
        g.sql_conn.close()
    except AttributeError:
        pass

# Default page/homepage
@app.route('/')
def homepage():
    return render_template('Homepage.html')

# GET all school rankings
@app.route('/api/v1/SchoolRankings', methods=['GET'])
def get_school_rankings_and_info():
    curs = g.sql_conn.cursor()
    query = 'SELECT i.School_Name, r.Rank, r.Avg_Standard_Score, i.Street_Address, i.City, i.State, i.Lat, i.Long \
            FROM school_rankings.dbo.School_Info as i \
                JOIN school_rankings.dbo.School_Rankings as r on r.School_ID = i.School_ID'
    curs.execute(query)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))
    return json.dumps(data, indent=4, sort_keys=True, default=str)

# GET rankings for one school
@app.route('/api/v1/SchoolRankings/<string:school_id>', methods=['GET'])
def get_single_school_data(school_id):
    curs = g.sql_conn.cursor()
    curs.execute("SELECT i.School_Name, r.Rank, r.Avg_Standard_Score, i.Lat, i.Long \
                    FROM school_rankings.dbo.School_Info as i \
                        JOIN school_rankings.dbo.School_Rankings as r on r.School_ID = i.School_ID \
                    WHERE i.school_id = ?", school_id)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))

    return json.dumps(data, indent=4, sort_keys=True, default=str)

# POST data to school information table
@app.route('/api/v1/SchoolInformation', methods=['POST'])
def insertnew():
    data = request.get_json()

    curs = g.sql_conn.cursor()

    query = 'insert school_rankings.dbo.School_Info (School_ID, School_Name, Street_Address, State, Zip) VALUES (?,?,?,?,?,?,?)'

    if isinstance(data, dict):
        curs.execute(query, data["School_ID"], data["School_Name"], data["Street_Address"], data["City"], data["State"], data["Zip"], data["Lat"], data["Long"])
        curs.commit()

    if isinstance(data, list):
        for row in data:
            curs.execute(query,row["School_ID"], row["School_Name"], row["Street_Address"], row["City"], row["State"], row["Zip"], row["Lat"], row["Long"])
            curs.commit()

    return 'Success', 200

# DELETE a school's information
@app.route('/api/v1/SchoolInformation/<string:school_id>', methods=['DELETE'])
def delete_school(school_id):
    curs = g.sql_conn.cursor()
    curs.execute('DELETE FROM school_rankings.dbo.School_Info WHERE school_ID = ?', school_id)

    return 'Success', 200

if __name__ == '__main__':
    app.run()