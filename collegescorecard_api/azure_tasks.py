from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os 
from dotenv import load_dotenv 

load_dotenv()
BLOB_SAS_TOKEN = os.getenv("BLOB_SAS_TOKEN")
BLOB_SAS_URL = os.getenv("BLOB_SAS_URL")
BLOB_ACCOUNT_URL = os.getenv("BLOB_ACCOUNT_URL")

# Acquire a credential object
token_credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(
        account_url=BLOB_ACCOUNT_URL,
        credential=token_credential)

container_client = blob_service_client.get_container_client('destination')


