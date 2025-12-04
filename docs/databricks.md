## Setting Up Databricks

First you will need to enable the databricks connector in Azure under your resource group and subscription.

You can follow the [CLI tutorial here](https://docs.databricks.com/aws/en/dev-tools/cli/tutorial?language=Windows), install the Databricks CLI ```winget install Databricks.DatabricksCLI```.

Then run ```databricks auth login --host <your-workbook-url>``` and follow the gateway, you should now be authenticated with your databricks env.
