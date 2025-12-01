# Cryptocurrency-Data
End-to-End data platform ingesting raw data from api to demonstrate ETL process.

## Setting Up Your Environment

If you want to emulate this project on your machine it is recommended to use a virtual environment using python venv -> ```python -m venv venv -r requirements```.

## Data Source 

The data used in this project was sourced from the official U.S Department of Education api [here](https://collegescorecard.ed.gov/data). You can also request an api key under [API Access and Authentication](https://collegescorecard.ed.gov/data/api-documentation).

## Intention 

It is our goal in this project to demonsrate a sort of end-to-end ETL process with Bi capabilities, specifically with Data Bricks and Power BI in mind. 

### Cloud Platform 

Databricks is cloud platform independant, we use Microsoft Azure in this project.
To download the CLI for Azure, you will need to install using ```winget install --exact --id Microsoft.AzureCLI```.
You can then log in to Azure using ```az login``` in power shell.

### Cloud Authentication

Follow the authentication guide [here](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli?view=azure-cli-latest) to set up your Azure CLI environemnt that you installed.
You are going to have to set up your own azure container delta lake. 

### Local Development Authentication 

Once you have downloaded and authenticated Azure in your cmd, you need to [authenticate your python app](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/local-development-service-principal?tabs=azure-cli).

## Rate-Limits 

Unfortunately the documentation does not specify when the rate-limit resets so we are going to assume it resets per UTC hour. The rate limit per reset is 1000 requests which is generous but there are precautions taken to help ensure this it is not exceeded.  
