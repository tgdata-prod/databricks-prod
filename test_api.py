import requests
from dotenv import load_dotenv
import os 
import json 
import time 
from datetime import datetime


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
    all_data = []    

    last_execution_time = datetime.fromisoformat(last_execution_data['last_execution_time'])
    api_call_count = last_execution_data['api_call_count']
    
    
    url = f'https://api.data.gov/ed/collegescorecard/v1/schools?api_key={COLLEGESCORE_API_KEY}'
    
    page = 0
    total_pages = 0 
    while page<=total_pages:
        http_params.update('')
        status = requests.get(url, http_params, timeout=60)

        if status and status.status_code==200:
            try:      
                #Rate Limit (https://collegescorecard.ed.gov/data/api-documentation/)  
                if (datetime.now()-last_execution_time).min<60 and api_call_count<1000:
                    api_call_count += 1 
                else: 
                    raise Exception('You have reached the api call limit')
            except requests.HTTPError.strerror as e:
                print(e)
                    
        content = json.loads(status.content)

        metadata = content['metadata']
        page, total_pages = metadata['page'], metadata['total']
        

        results = content['results'][0]

        all_data.append(results)
        page = page + 1
        time.sleep(0.5)
        
    return all_data
