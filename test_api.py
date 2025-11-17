import requests
from dotenv import load_dotenv
import os 
import json 
import time 
from datetime import datetime,timedelta
import sys

#api_execution_data is json object
def get_university_data_http(**http_params):
        
    load_dotenv()

    COLLEGESCORE_API_KEY =  os.getenv("COLLEGESCORE_API_KEY")

    if os.path.exists('./api_execution_data.json'): 
        with open('./api_execution_data.json', 'r') as file:
            api_execution_data = json.load(file)        
            last_execution_time = api_execution_data['last_execution_time']
            api_call_count = api_execution_data['api_call_count']        
    else: 
        last_execution_time = datetime.now()
        api_call_count = 0        

    
    all_data = dict()
    
    url = f'https://api.data.gov/ed/collegescorecard/v1/schools?api_key={COLLEGESCORE_API_KEY}'

    status = requests.get(url, params=http_params)

    print(status)

    # if status:
    #     if (datetime.now().minute-last_execution_time.minute)<60 and api_call_count<1000:
    #         api_call_count += 1 
    #     else: 
    #         raise Exception('You have reached the api call limit')
            



    # metadata = status['metadata']
    # current_page, total_pages = metadata['page'], metadata['total']



    # while current_page<total_pages:

    #     status = requests.get(url, params=http_params)

    #     response = status.content

    #     response_pretty = json.loads(response)

    #     if response_pretty:
    #         try:
    #             results = response_pretty['results']
    #         except json.JSONDecodeError as e:
    #             print("object is empty")    

        
    
    #     new_metadata = response_pretty['metadata']
    #     current_page = new_metadata['current_page']
    #     api_call_count+=1
    #     all_data.update(results)
    #     time.sleep(0.5)

    
    # new_api_execution_data = {'last_execution_time': datetime.now(), \
    #                           'api_call_count': api_call_count}

    # with open('./api_execution_data.json', 'w'):
    #     json.dump(new_api_execution_data)

    

    # return all_data
