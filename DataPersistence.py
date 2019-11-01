import pyodbc
import json
import requests

################
# GETTING DATA #
################

# Get the first page of data and wait ~one minute
high_school_rankings_page_1 = requests.get(f'https://api.schooldigger.com/v1.2/rankings/schools/UT?level=High&perPage=50&appID=95713b9f&appKey=f18f10f88b5d17a6f0b986cfbbbdd446')
#time.sleep(75)

# Get the second page of data and wait ~one minute
high_school_rankings_page_2 = requests.get(f'https://api.schooldigger.com/v1.2/rankings/schools/UT?level=High&perPage=50&page=2&appID=95713b9f&appKey=f18f10f88b5d17a6f0b986cfbbbdd446')
#time.sleep(75)

# Get the third page of data - don't need to wait a minute this time
high_school_rankings_page_3 = requests.get(f'https://api.schooldigger.com/v1.2/rankings/schools/UT?level=High&perPage=50&page=3&appID=95713b9f&appKey=f18f10f88b5d17a6f0b986cfbbbdd446')

# Place into list containing dictionary
school_list = []
school_list.append(json.loads(high_school_rankings_page_1.text)['schoolList'])
school_list.append(json.loads(high_school_rankings_page_2.text)['schoolList'])
school_list.append(json.loads(high_school_rankings_page_3.text)['schoolList'])

# Testing out how to access the correct data. Use for reference in lines 59 - 65
print(school_list[0][0]["schoolid"], school_list[0][0]["schoolName"], school_list[0][0]["rankHistory"][0]["rank"], school_list[0][0]["rankHistory"][0]["averageStandardScore"])

print(school_list[1][1]["schoolid"], school_list[1][1]["schoolName"], school_list[1][1]["rankHistory"][0]["rank"], school_list[1][1]["rankHistory"][0]["averageStandardScore"])

print(school_list[2][2]["schoolid"], school_list[2][2]["schoolName"], school_list[2][2]["rankHistory"][0]["rank"], school_list[2][2]["rankHistory"][0]["averageStandardScore"])



###################
# PERSISTING DATA #
###################

# Set connection string for MIS5400 Database
connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:mis5440eg.database.windows.net,1433;Database=MIS5400Project;Uid=elsagreenwalt;Pwd=Mis5400fa2019;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Return connection object
conn = pyodbc.connect(connection_string, autocommit=True)

# Create Cursor
curs = conn.cursor()

# Create our staging table
# curs.execute(
#     '''
#     create table MIS_5400_staging_table(
#     School_ID nvarchar(100) primary key
#     ,School_Name varchar(100)
#     ,Rank int
#     ,Average_Standard_Score float
#     )
#
#     '''
#     )

# Insert our data
insert_query = 'insert into MIS_5400_staging_table (School_ID, School_Name, Rank, Average_Standard_Score) values (?,?,?,?)' # Question marks as placeholders
#TODO figure out why this is only inserting three rows
rows_to_insert = []
for i in range(0, len(school_list)):
    school_id = school_list[i][i]["schoolid"]
    school_name = school_list[i][i]["schoolName"]
    school_rank = school_list[i][i]["rankHistory"][0]["rank"]
    school_score = school_list[i][i]["rankHistory"][0]["averageStandardScore"]
    row = (school_id, school_name, school_rank, school_score)
    rows_to_insert.append(row)
curs.executemany(insert_query, rows_to_insert)

# with open(r'/tmp/data/todayilearned.json') as data_file:
#     data = json.load(data_file)
#     data_list = data['data']['children']
#     rows_to_insert = []
#     for entry in data_list:
#         rows_to_insert.append(tuple([entry['data']['title'], entry['data']['domain']]))
#     curs.executemany(insert_query, rows_to_insert)


# Commit
conn.commit()
# Close
conn.close



