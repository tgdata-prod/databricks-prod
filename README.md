# Cryptocurrency-Data
End-to-End data platform ingesting raw data from api to demonstrate ETL process.

## Setting Up Your Environment

If you want to emulate this project on your machine it is recommended to use a virtual environment using python venv -> ```python -m venv venv``` then ```pip install -r requirements.txt```.

## Data Source 

The data used in this project was sourced from the official U.S Department of Education api [here](https://collegescorecard.ed.gov/data). You can also request an api key under [API Access and Authentication](https://collegescorecard.ed.gov/data/api-documentation).

## Intention 

It is our goal in this project to demonsrate a sort of end-to-end ETL process with Bi capabilities, specifically with Data Bricks and Power BI in mind. 

## Azure Cloud 

Databricks is cloud platform independant, we use Microsoft Azure in this project.
To download the CLI for Azure, you will need to install using ```winget install --exact --id Microsoft.AzureCLI```.

### Authenticating your app with Azure Quickstart

Before you can authenticate locally you need to [create an account with Azure](https://azure.microsoft.com/en-au/pricing/purchase-options/azure-account?icid=azurefreeaccount). 

You then need to create a resource group and under that a storage account with Hierarchical Namespace turned on.

You can then log in to Azure using ```az login``` in the cli, there should be a default subscription that is created when you first make an account with azure and you can find it using ```az account list``` under "name".
Once you have your subscription name, you can run ```az account get-access-token --subscription "<subscription ID or name>"``` to recieve your JWT, you don't need to store this token as it is stored when you run ```az login```.

You now have two choices to authenticate your python application, you can either use a [service principal](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-local-development-service-principal) or create a [dev account](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/local-development-dev-accounts?tabs=azure-cli%2Csign-in-azure-cli). In this project, we use a dev account because we may want to onboard other developers in the future instead of making service principals for every developer. The downside of this approach however is developers may have more perms than they require so it is recommended for small teams. 

[This image](https://learn.microsoft.com/en-us/azure/developer/python/sdk/media/local-dev-dev-accounts-overview.png) demonstrates how applciation authentication works in azure. 

You now have to create a security group for the account using; 
```az ad group create --display-name <display name here> --mail-nickname <mail nickname here> --description "security group to manage our python application"```.

The cmdlet should out-put an "id" we will need, if you want to request it again, use; 
```az ad group show --group "<display name here>" --query id --output tsv```.
You may also want to add this to your .env as per the .env.example <MICROSOFT_ENTRA_SECURITY_GROUP_ID_HERE>.

You can now get the users Object Id using [```az ad user list```](https://learn.microsoft.com/en-us/cli/azure/ad/sp?view=azure-cli-latest#az-ad-user-list) for the dev you want to add.

This will give you their Object Id and you can use it to now add them to the group; 
```az ad group member add --group <display name here> --member-id <user-object-id>``` 

### Assigning roles to your group

Now you have created an Entra group and added users to it, you can now assign the roles and scope for the group.
Refer to [Assign roles to the Microsoft Entra group](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/local-development-dev-accounts) to edit roles and scope as you prefer.

to make the group a blob contributer for our storage account, run;
```az role assignment create --assignee "<group-object-id or group-principal-name>" --role "Storage Blob Data Contributor" --scope "/subscriptions/<sub-id>/resourceGroups/<resourcegroup-name>/providers/Microsoft.Storage/storageAccounts/<account-name>"```

To get the in-use subscription id, use ```az account show --query id --output tsv```

## Setting Up Databricks

First you will need to enable the databricks connector in Azure under your resource group and subscription.

You can follow the [CLI tutorial here](https://docs.databricks.com/aws/en/dev-tools/cli/tutorial?language=Windows), install the Databricks CLI ```winget install Databricks.DatabricksCLI```.

then run ```databricks auth login --host <your-workbook-url>```.



You may need to




## Rate-Limits 

Unfortunately the documentation does not specify when the rate-limit resets so we are going to assume it resets per UTC hour. The rate limit per reset is 1000 requests which is generous but there are precautions taken to help ensure this it is not exceeded.  
