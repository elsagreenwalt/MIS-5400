import pyodbc
import json
import requests
import time

################
# GETTING DATA #
################

# Get the first page of data and wait ~one minute
high_school_rankings_page_1 = requests.get(f'https://api.schooldigger.com/v1.2/rankings/schools/UT?level=High&perPage'
                                           f'=50&appID=95713b9f&appKey=f18f10f88b5d17a6f0b986cfbbbdd446')
# time.sleep(75)

# Get the second page of data and wait ~one minute
high_school_rankings_page_2 = requests.get(f'https://api.schooldigger.com/v1.2/rankings/schools/UT?level=High&perPage'
                                           f'=50&page=2&appID=95713b9f&appKey=f18f10f88b5d17a6f0b986cfbbbdd446')
# time.sleep(75)

# Get the third page of data - don't need to wait a minute this time
high_school_rankings_page_3 = requests.get(f'https://api.schooldigger.com/v1.2/rankings/schools/UT?level=High&perPage'
                                           f'=50&page=3&appID=95713b9f&appKey=f18f10f88b5d17a6f0b986cfbbbdd446')

# Place into list containing dictionary
school_list = []
school_list.append(json.loads(high_school_rankings_page_1.text)['schoolList'])
school_list.append(json.loads(high_school_rankings_page_2.text)['schoolList'])
school_list.append(json.loads(high_school_rankings_page_3.text)['schoolList'])


###################
# PERSISTING DATA #
###################

# Set connection string for MIS5400 Database
connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:mis5440eg.database.windows.net,' \
                    '1433;Database=MIS5400Project;Uid=elsagreenwalt;Pwd=Mis5400fa2019;Encrypt=yes' \
                    ';TrustServerCertificate=no;Connection Timeout=30; '

# Return connection object
conn = pyodbc.connect(connection_string, autocommit=True)

# Create Cursor
curs = conn.cursor()

# Create our staging table if it doesn't exist
if curs.tables(table='MIS_5400_staging_table', tableType='TABLE').fetchone():
    None
else:
    curs.execute(
        '''
        create table MIS_5400_staging_table(
        School_ID nvarchar(100) primary key
        ,School_Name varchar(100)
        ,Rank int
        ,Average_Standard_Score float
        )

        '''
    )

# Set up insert query
insert_query = 'insert into MIS_5400_staging_table (School_ID, School_Name, Rank, Average_Standard_Score) \
                values (?,?,?,?)'  # Question marks as placeholders

# TODO figure out how to get this into one for loop
# Insert the first page
rows_to_insert = []
for i in range(0, len(school_list[0])):
    school_id = school_list[0][i]["schoolid"]
    school_name = school_list[0][i]["schoolName"]
    school_rank = school_list[0][i]["rankHistory"][0]["rank"]
    school_score = school_list[0][i]["rankHistory"][0]["averageStandardScore"]
    row = (school_id, school_name, school_rank, school_score)
    rows_to_insert.append(row)
curs.executemany(insert_query, rows_to_insert)

# Insert the second page
rows_to_insert = []
for i in range(0, len(school_list[1])):
    school_id = school_list[1][i]["schoolid"]
    school_name = school_list[1][i]["schoolName"]
    school_rank = school_list[1][i]["rankHistory"][0]["rank"]
    school_score = school_list[1][i]["rankHistory"][0]["averageStandardScore"]
    row = (school_id, school_name, school_rank, school_score)
    rows_to_insert.append(row)
curs.executemany(insert_query, rows_to_insert)

# Insert the third page
rows_to_insert = []
for i in range(0, len(school_list[2])):
    school_id = school_list[2][i]["schoolid"]
    school_name = school_list[2][i]["schoolName"]
    school_rank = school_list[2][i]["rankHistory"][0]["rank"]
    school_score = school_list[2][i]["rankHistory"][0]["averageStandardScore"]
    row = (school_id, school_name, school_rank, school_score)
    rows_to_insert.append(row)
curs.executemany(insert_query, rows_to_insert)

# Commit
conn.commit()
# Close
conn.close



