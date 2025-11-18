import requests
from dotenv import load_dotenv
import os 
import json 
import time 
from datetime import datetime,timedelta
import sys


def write_api_execution_data(new_api_execution_data: dict ,json_file_path='./api_execution_data.json'):
    with open(json_file_path, 'w') as file:
        json.dump(new_api_execution_data, file)


def load_api_execution_data(json_file_path='./api_execution_data.json') -> dict:  

    if os.path.exists(json_file_path): 
        with open(json_file_path, 'r') as file:
            api_execution_data = json.load(file)
            last_execution_time = api_execution_data['last_execution_time']
            api_call_count = api_execution_data['api_call_count'] 
        return {'last_execution_time':last_execution_time, 'api_call_count':api_call_count}   
    else: 
        last_execution_time = datetime.now().isoformat()
        api_call_count = 0   
    return {'last_execution_time':last_execution_time, 'api_call_count':api_call_count}


def get_university_data_http(http_params: dict, last_execution_data: dict):
    
    load_dotenv()
    COLLEGESCORE_API_KEY =  os.getenv("COLLEGESCORE_API_KEY")
    all_data = dict()    

    last_execution_time = datetime.fromisoformat(last_execution_data['last_execution_time'])
    api_call_count = last_execution_data['api_call_count']
    
    
    url = f'https://api.data.gov/ed/collegescorecard/v1/schools?api_key={COLLEGESCORE_API_KEY}'
    

    status = requests.get(url, params=http_params)
    
    if status and status.status_code==200:
        try:        
            if (datetime.now().minute-last_execution_time.minute)<60 and api_call_count<1000:
                api_call_count += 1 
            else: 
                raise Exception('You have reached the api call limit')
        except requests.HTTPError.strerror as e:
            print(e)
                
    content = json.loads(status.content)

    metadata = content['metadata']
    page, total_pages, per_page = metadata['page'], metadata['total'], metadata['perpage']



    while current_page<total_pages:

        status = requests.get(url, params=http_params)

        response = status.content

        response_pretty = json.loads(response)

        if response_pretty:
            try:
                results = response_pretty['results']
            except json.JSONDecodeError as e:
                print("object is empty")    

        
    
        new_metadata = response_pretty['metadata']
        current_page = new_metadata['current_page']
        api_call_count+=1
        all_data.update(results)
        time.sleep(0.5)

    
    # new_api_execution_data = {'last_execution_time': datetime.now(), \
    #                           'api_call_count': api_call_count}


    

    # return all_data
