import requests
from dotenv import load_dotenv
import os 
import json 
import time 
from datetime import datetime, timedelta
import pytz

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


def get_university_data_http(http_params: dict, last_execution_data: dict):
    
    load_dotenv()
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
        status = requests.get(url, http_params, timeout=30)
        status.raise_for_status()
        api_call_count+=1


        if not status or not status.status_code==200:
            print(f'http error occured with code {status.status_code}')
            break
                    
        content = json.loads(status.content)


        metadata = content['metadata']
        
        total_pages = metadata['total']
    
        if abs(total_pages-api_call_count)>999:
            print('too many pages to load')
            break

        results = content.get('results', {})
        if not results:
            print('no results')
            break
        if len(results)>1:
            print('larger dimension of results than expected')
            break 
        else:
            results = results[0]
        
        all_data.append(results)
        page = page + 1
        print(f'page is {page} total pages is {total_pages}\n---------------------------')    


        if page>=total_pages or page > 10:
            print('\n\nall pages cycled')
            new_api_execution_data = {'last_execution_time_utc': utc_now.isoformat(), 'api_call_count': api_call_count} 
            write_api_execution_data(new_api_execution_data)
            print(f'last executed {new_api_execution_data}')
            print(f'time in mins until refresh {(last_execution_time_utc_last_reset+timedelta(hours=1))-utc_now}')        
            return all_data, metadata

        time.sleep(0.5)
    new_api_execution_data = {'last_execution_time': utc_now.astimezone(tz=pytz.timezone('Australia/Melbourne')).isoformat(), 'api_call_count': api_call_count}  
    write_api_execution_data(new_api_execution_data)
    