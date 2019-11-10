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
time.sleep(75)

# Get the second page of data and wait ~one minute
high_school_rankings_page_2 = requests.get(f'https://api.schooldigger.com/v1.2/rankings/schools/UT?level=High&perPage'
                                           f'=50&page=2&appID=95713b9f&appKey=f18f10f88b5d17a6f0b986cfbbbdd446')
time.sleep(75)

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
connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:mis5400schooldata.database.windows.net,1433;Database=school_rankings;Uid=elsagreenwalt;\
                    Pwd=Mis5400fa2019;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Return connection object
conn = pyodbc.connect(connection_string, autocommit=True)

# Create Cursor
curs = conn.cursor()

# Create our school info table if it doesn't exist
if curs.tables(table='School_Info', tableType='TABLE').fetchone():
    None
else:
    curs.execute(
        '''
        create table School_Info(
        School_ID nvarchar(100) primary key
        ,School_Name varchar(100)
        ,Street_Address varchar(100)
        ,State varchar(100)
        ,Zip varchar(20)
        )

        '''
    )

# Create our school rankings table if it doesn't exist
if curs.tables(table='School_Rankings', tableType='TABLE').fetchone():
    None
else:
    curs.execute(
        '''
        create table School_Rankings(
        School_ID nvarchar(100) primary key
        ,Rank int
        ,Avg_Standard_Score varchar(100)
        )

        '''
    )

add_data = input("Yes/No: Would you like to add data to the database? ")

if add_data == 'Yes':
    # Set up insert query for School_Info table
    insert_query = 'insert into School_Info (School_ID, School_Name, Street_Address, State, Zip) \
                    values (?,?,?,?,?)'  # Question marks as placeholders

    # TODO figure out how to get this into one for loop
    # Insert the first page
    rows_to_insert = []
    for i in range(0, len(school_list[0])):
        school_id = school_list[0][i]["schoolid"]
        school_name = school_list[0][i]["schoolName"]
        street_address = school_list[0][i]["address"]["street"]
        state = school_list[0][i]["address"]["state"]
        zip = school_list[0][i]["address"]["zip"]
        row = (school_id, school_name, street_address, state, zip)
        rows_to_insert.append(row)
    curs.executemany(insert_query, rows_to_insert)

    # Insert the second page
    rows_to_insert = []
    for i in range(0, len(school_list[1])):
        school_id = school_list[1][i]["schoolid"]
        school_name = school_list[1][i]["schoolName"]
        street_address = school_list[1][i]["address"]["street"]
        state = school_list[1][i]["address"]["state"]
        zip = school_list[1][i]["address"]["zip"]
        row = (school_id, school_name, street_address, state, zip)
        rows_to_insert.append(row)
    curs.executemany(insert_query, rows_to_insert)

    # Insert the third page
    rows_to_insert = []
    for i in range(0, len(school_list[2])):
        school_id = school_list[2][i]["schoolid"]
        school_name = school_list[2][i]["schoolName"]
        street_address = school_list[2][i]["address"]["street"]
        state = school_list[2][i]["address"]["state"]
        zip = school_list[2][i]["address"]["zip"]
        row = (school_id, school_name, street_address, state, zip)
        rows_to_insert.append(row)
    curs.executemany(insert_query, rows_to_insert)


    # Set up insert query for School_Rankings table
    insert_query = 'insert into School_Rankings (School_ID, Rank, Avg_Standard_Score) \
                    values (?,?,?)'  # Question marks as placeholders

    # TODO figure out how to get this into one for loop
    # Insert the first page
    rows_to_insert = []
    for i in range(0, len(school_list[0])):
        school_id = school_list[0][i]["schoolid"]
        school_rank = school_list[0][i]["rankHistory"][0]["rank"]
        school_score = school_list[0][i]["rankHistory"][0]["averageStandardScore"]
        row = (school_id, school_rank, school_score)
        rows_to_insert.append(row)
    curs.executemany(insert_query, rows_to_insert)

    # Insert the second page
    rows_to_insert = []
    for i in range(0, len(school_list[1])):
        school_id = school_list[1][i]["schoolid"]
        school_rank = school_list[1][i]["rankHistory"][0]["rank"]
        school_score = school_list[1][i]["rankHistory"][0]["averageStandardScore"]
        row = (school_id, school_rank, school_score)
        rows_to_insert.append(row)
    curs.executemany(insert_query, rows_to_insert)

    # Insert the third page
    rows_to_insert = []
    for i in range(0, len(school_list[2])):
        school_id = school_list[2][i]["schoolid"]
        school_rank = school_list[2][i]["rankHistory"][0]["rank"]
        school_score = school_list[2][i]["rankHistory"][0]["averageStandardScore"]
        row = (school_id, school_rank, school_score)
        rows_to_insert.append(row)
    curs.executemany(insert_query, rows_to_insert)

    # Commit
    conn.commit()
    # Close Connection
    conn.close
else:
    None




