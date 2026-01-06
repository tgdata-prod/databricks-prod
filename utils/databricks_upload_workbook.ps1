. ./load_dotenv.ps1

$WORKSPACE=$env:WORKSPACE

databricks workspace import $WORKSPACE --file ./databricks/TomsNotebook.ipynb --language PYTHON --overwrite --format
