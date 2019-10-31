import pyodbc
import csv
import json

# Set connection string for MIS5400 Database
connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:mis5440eg.database.windows.net,1433;Database=MIS5400Project;Uid=elsagreenwalt;Pwd=Mis5400fa2019;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Return connection object
conn = pyodbc.connect(connection_string,autocommit=True)

# Create Cursor
curs = conn.cursor()

# Create our staging table
curs.execute(
    '''
    create table MIS_5400_staging_table(
    School_ID int primary key
    ,School_Name string
    ,Rank int
    )

    '''
    )

# Insert our data
insert_query = 'insert into MIS_5400_staging_table (School_ID, School_Name, Ranking) values (?,?)' # Question marks as placeholders
#TODO update this to reflect our json data
with open(r'/tmp/data/todayilearned.json') as data_file:
    data = json.load(data_file)
    data_list = data['data']['children']
    rows_to_insert = []
    for entry in data_list:
        rows_to_insert.append(tuple([entry['data']['title'], entry['data']['domain']]))
    curs.executemany(insert_query, rows_to_insert)


# Commit
conn.commit()
# Close
conn.close



