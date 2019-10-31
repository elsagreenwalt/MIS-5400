import requests
import pprint
import time
import json

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


print(school_list[0][0]["schoolid"],school_list[0][0]["schoolName"],school_list[0][0]["rankHistory"][0]["rank"],school_list[0][0]["rankHistory"][0]["averageStandardScore"])




#Data Description
#   This data includes a list of high schools in Utah, their rankings, and their demographics.
#   There are 128 rows of data (128 high schools). The data all seems valid and reliable, but there is one concern - we are only allowed 1 API call per minute and 20 per day,
#   which is problematic because we need to make multiple API calls to get all pages of data. We need to figure out a way to make the calls one at a time
#   and store the responses in one location.

# Worked with Rim Dahhou.