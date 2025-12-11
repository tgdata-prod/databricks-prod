## Setting Up Databricks

First you will need to enable the databricks connector in Azure under your resource group and subscription.

You can follow the [CLI tutorial here](https://docs.databricks.com/aws/en/dev-tools/cli/tutorial?language=Windows), install the Databricks CLI ```winget install Databricks.DatabricksCLI```.

Create a notebook in databricks then run ```databricks auth login --host <your-workbook-url>``` locally and follow the gateway, you should now be authenticated with your databricks workbook env.

then run ```databricks configure``` to generate your credentials. You will need to generate a personal token and enter you host name <https://your-host.azuredatabricks.net>.

If you want to upload a new databricks notebook from local you can use the databricks_upload_workbook.ps1 in utils.

To run your spark clusters locally, it is recommended you make sure your local spark version is the same as the remote databricks version ```print(spark.version)```.

You also need to make sure your [databricks-connect and python version](https://docs.databricks.com/aws/en/dev-tools/databricks-connect/requirements) are compatable.


You will aslo need to create a service principal for the Databricks application to access our datalake via the [App registrations](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)
