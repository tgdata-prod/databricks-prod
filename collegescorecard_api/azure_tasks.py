import sys
#Temp path set for testing
sys.path[0] = 'C:\\Users\\lette\\projects\\Cryptocurrency-Data'
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os 
from dotenv import load_dotenv 
from collegescorecard_api.api import get_university_data_http 
from utils.str_utils import make_stringlist_from_list
import csv

load_dotenv()
BLOB_SAS_TOKEN = os.getenv("BLOB_SAS_TOKEN")
BLOB_SAS_URL = os.getenv("BLOB_SAS_URL")
BLOB_ACCOUNT_URL = os.getenv("BLOB_ACCOUNT_URL")

# Acquire a credential object
token_credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(
        account_url=BLOB_ACCOUNT_URL,
        credential=token_credential)


blob_client = blob_service_client.get_blob_client(container='destination',blob='university_data.csv')
container_client = blob_service_client.get_container_client(container='destination')

fields= ['id', 'school.name', 'school.state', 'latest.student.size', 
        'latest.cost.tuition.in_state', 'latest.cost.tuition.out_of_state']

str_obj = make_stringlist_from_list(list=fields)

http_params = {'school.name': 'Harvard University','fields': str_obj}

data = get_university_data_http(http_params)


with open(f'./collegescorecard_api/university_data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)

if not os.path.exists(f'./collegescorecard_api/university_data.csv'):
        raise Exception('file was not written')        
container_client.delete_blob('university_data.csv')
blob_client.upload_blob(f'./collegescorecard_api/university_data.csv')
        
os.remove(f'./collegescorecard_api/university_data.csv')
