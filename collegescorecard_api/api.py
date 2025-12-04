import requests
from dotenv import load_dotenv
import os 
import json 
import time 
from datetime import datetime, timedelta
import pytz
from tenacity import retry, retry_if_not_exception_type, wait_exponential, stop_after_attempt, stop_after_delay  
from urllib.error import HTTPError

def write_api_execution_data(new_api_execution_data: dict ,json_file_path='./api_execution_data.json'):
    with open(json_file_path, 'w') as file:
        json.dump(new_api_execution_data, file)

def load_api_execution_data(json_file_path='./api_execution_data.json') -> dict:  

    if os.path.exists(json_file_path): 
        with open(json_file_path, 'r') as file:
            api_execution_data = json.load(file)
            last_execution_time_utc = api_execution_data['last_execution_time_utc']
            api_call_count = api_execution_data['api_call_count'] 
        return {'last_execution_time_utc':last_execution_time_utc, 'api_call_count':api_call_count}   
    else: 
        last_execution_time_utc = datetime.astimezone(datetime.now(),tz=pytz.utc).isoformat()
        api_call_count = 0   
    return {'last_execution_time_utc':last_execution_time_utc, 'api_call_count':api_call_count}

@retry(
        stop=stop_after_attempt(3) | stop_after_delay(30),
        wait=wait_exponential(multiplier=2, max=120),   
        retry=retry_if_not_exception_type(HTTPError)
)
#potential http params reference (https://collegescorecard.ed.gov/data/api-documentation/)
def get_university_data_http(http_params: dict):
    
    load_dotenv()
    last_execution_data = load_api_execution_data()
    COLLEGESCORE_API_KEY =  os.getenv("COLLEGESCORE_API_KEY")
    url = f'https://api.data.gov/ed/collegescorecard/v1/schools?api_key={COLLEGESCORE_API_KEY}'

    
    all_data = []    

    last_execution_time_utc = datetime.fromisoformat(last_execution_data['last_execution_time_utc'])
    last_execution_time_utc_last_reset = last_execution_time_utc.replace(minute=0, second=0)

    api_call_count = last_execution_data['api_call_count']
        
    utc_now = datetime.astimezone(datetime.now(),tz=pytz.utc)    
    time_delta_mins = (utc_now-last_execution_time_utc_last_reset).total_seconds()/60
    print(f'time delta since last rate-limit reset: {time_delta_mins}')
    #Rate Limit (https://collegescorecard.ed.gov/data/api-documentation/)  
    if not api_call_count<1000 and time_delta_mins < 60:
        raise Exception('You have reached the api call limit')
    if time_delta_mins>=60:
        api_call_count=0
    
    page=0
    while True:    

        print('commencing fetch\n')
        http_params.update({'per_page': 100, 'page': page})
        status = requests.get(url, http_params, timeout=30)
        status.raise_for_status()
        api_call_count+=1
        new_api_execution_data = {'last_execution_time_utc': utc_now.isoformat(), 'api_call_count': api_call_count}   
        write_api_execution_data(new_api_execution_data)

        if not status or not status.status_code==200:
            raise Exception(f'http error occured with code {status.status_code}')
            
                    
        content = json.loads(status.content)

        metadata = content['metadata']
        
        total_pages = metadata['total']
    
        if abs(total_pages-api_call_count)>999:
            raise Exception('too many pages to load in accordance with rate limit')
            

        results = content.get('results', {})
        
        
        if not results:
            raise Exception('no results')
            
        
        all_data.append(results)
        page = page + 1
        print(f'page is {page}, total pages is {total_pages}\n---------------------------')    

        if page>=total_pages:
            print('\n\nall pages cycled')
            print(f'last executed {new_api_execution_data}')
            print(f'time in mins until refresh {((last_execution_time_utc_last_reset+timedelta(hours=1))-utc_now).total_seconds()/60}')  
                    
            return all_data
        time.sleep(0.5)
