# Cryptocurrency-Data
End-to-End data platform ingesting raw data from api to demonstrate ETL process.

## Setting Up Your Environment

If you want to emulate this project on your machine it is recommended to use a virtual environment using python venv -> ```python -m venv venv``` then ```pip install -r requirements.txt```.

## Data Source 

The data used in this project was sourced from the official U.S Department of Education api [here](https://collegescorecard.ed.gov/data). You can also request an api key under [API Access and Authentication](https://collegescorecard.ed.gov/data/api-documentation).

## Intention 

It is our goal in this project to demonsrate a sort of end-to-end ETL process with Bi capabilities, specifically with Data Bricks and Power BI in mind.
It will go through most of everything from setting up cloud environments and creating pipelines with medallion architecture.  

## Rate-Limits 

Unfortunately the documentation does not specify when the rate-limit resets so we are going to assume it resets per UTC hour. The rate limit per reset is 1000 requests which is generous but there are precautions taken to help ensure this it is not exceeded.  
