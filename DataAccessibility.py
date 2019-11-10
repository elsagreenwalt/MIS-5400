from flask import Flask, g, render_template, abort, request
import json
import pyodbc

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

# GET all school data
@app.route('/api/v1/schools', methods=['GET'])
def get_school_data():
    curs = g.sql_conn.cursor()
    query = 'select * from school_rankings.dbo.School_Info'
    curs.execute(query)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))
    return json.dumps(data, indent=4, sort_keys=True, default=str)



# GET all school rankings
@app.route('/api/v1/rankings', methods=['GET'])
def get_school_rankings():
    curs = g.sql_conn.cursor()
    query = 'select * from school_rankings.dbo.School_Rankings'
    curs.execute(query)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))
    return json.dumps(data, indent=4, sort_keys=True, default=str)


# GET information for one school
@app.route('/api/v1/schools/<string:school_id>', methods=['GET'])
def get_single_school_data(school_id):
    curs = g.sql_conn.cursor()
    curs.execute("select * from school_rankings.dbo.School_Info where school_id = ?", school_id)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))

    return json.dumps(data, indent=4, sort_keys=True, default=str)

# GET ranking for one school
@app.route('/api/v1/rankings/<string:school_id>', methods=['GET'])
def get_single_school_ranking(school_id):
    curs = g.sql_conn.cursor()
    curs.execute("select * from school_rankings.dbo.School_Rankings where school_id = ?", school_id)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))

    return json.dumps(data, indent=4, sort_keys=True, default=str)

# GET all school rankings
@app.route('/api/v1/all', methods=['GET'])
def get_school_rankings_and_info():
    curs = g.sql_conn.cursor()
    query = 'SELECT i.School_Name, r.Rank, r.Avg_Standard_Score \
            FROM school_rankings.dbo.School_Info as i \
                JOIN school_rankings.dbo.School_Rankings as r on r.School_ID = i.School_ID'
    curs.execute(query)

    columns = [column[0] for column in curs.description]
    data = []

    for row in curs.fetchall():
        data.append(dict(zip(columns, row)))
    return json.dumps(data, indent=4, sort_keys=True, default=str)

if __name__ == '__main__':
    app.run()