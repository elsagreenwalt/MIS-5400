import requests
import pprint

high_school_rankings_page_1 = requests.get(f'https://api.schooldigger.com/v1.2/rankings/schools/UT?level=High&perPage=50&appID=95713b9f&appKey=f18f10f88b5d17a6f0b986cfbbbdd446')
high_school_rankings_page_2 = requests.get(f'https://api.schooldigger.com/v1.2/rankings/schools/UT?level=High&perPage=50&page=2&appID=95713b9f&appKey=f18f10f88b5d17a6f0b986cfbbbdd446')
high_school_rankings_page_3 = requests.get(f'https://api.schooldigger.com/v1.2/rankings/schools/UT?level=High&perPage=50&page=3&appID=95713b9f&appKey=f18f10f88b5d17a6f0b986cfbbbdd446')


printer = pprint.PrettyPrinter(indent=2)
printer.pprint(high_school_rankings_page_1.json())
printer.pprint(high_school_rankings_page_2.json())
printer.pprint(high_school_rankings_page_3.json())


#Data Description
#   This data includes a list of high schools in Utah, their rankings, and their demographics.
#   There are 128 rows of data (128 high schools). The data all seems valid and reliable, but there is one concern - we are only allowed 1 API call per minute and 20 per day,
#   which is problematic because we need to make multiple API calls to get all pages of data. We need to figure out a way to make the calls one at a time
#   and store the responses in one location.