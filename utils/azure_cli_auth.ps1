. ./utils/load_dotenv.ps1
Load-DotEnv

$azure_user = $env:AZURE_USERNAME
$AzCred = Get-Credential -UserName $azure_user
az login -u $AzCred.UserName -p $AzCred.GetNetworkCredential().Password
