from django.shortcuts import render, redirect
from pyspark.sql import SparkSession
from azure_integration import read_csv_from_blob, write_to_sql_server
from pyspark.sql.functions import col, when
import pyodbc
from azure.storage.blob import BlobServiceClient

def home(request):
    return render(request, 'home.html')


def upload_csv(request):
    if request.method == "POST":
        # get the uploaded CSV file
        csv_file = request.FILES.get("csv_file")
        
        # set Azure Blob Storage account credentials
        BLOB_ACCOUNT_NAME = "<your-storage-account-name>"
        BLOB_ACCOUNT_ACCESS_KEY = "<your-storage-account-access-key>"
        CONTAINER_NAME = "<your-container-name>"
        BLOB_NAME = csv_file.name
        
        # create a SparkSession
        spark = SparkSession.builder.appName("CSV to Blob").getOrCreate()
        
        # read the CSV file into a dataframe
        df = spark.read.csv(csv_file, header=True, inferSchema=True)
        
        # write the dataframe to Azure Blob Storage
        blob_service_client = BlobServiceClient(account_url=f"https://{BLOB_ACCOUNT_NAME}.blob.core.windows.net/", credential=BLOB_ACCOUNT_ACCESS_KEY)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_client = container_client.get_blob_client(BLOB_NAME)
        blob_client.upload_blob(df.toPandas().to_csv(index=False))
        
        # redirect to the process_csv view with the file path as a parameter
        return redirect("process_csv", file_path=f"{CONTAINER_NAME}/{BLOB_NAME}")
    
    return render(request, "upload_csv.html")






def process_csv(request):
    # set Azure Blob Storage account credentials
    BLOB_ACCOUNT_NAME = "<your-storage-account-name>"
    BLOB_ACCOUNT_ACCESS_KEY = "<your-storage-account-access-key>"
    CONTAINER_NAME = "<your-container-name>"
    FILE_PATH = "<your-csv-file-path>"
    
    # read the CSV file from Azure Blob Storage into a dataframe
    spark = SparkSession.builder.appName("CSV to SQL").getOrCreate()
    df = read_csv_from_blob(spark, BLOB_ACCOUNT_NAME, BLOB_ACCOUNT_ACCESS_KEY, CONTAINER_NAME, FILE_PATH)
    
    # rename columns dynamically
    column_map = {}
    for column in df.columns:
        new_name = request.GET.get(f"column_map_{column}")
        column_map[column] = new_name if new_name else column
    df = df.select([col(c).alias(column_map.get(c, c)) for c in df.columns])
    
    # filter data dynamically
    filter_col = request.GET.get("filter_col")
    filter_val = request.GET.get("filter_val")
    if filter_col and filter_val:
        df = df.filter(col(filter_col) == filter_val)
    
    # create a new column using existing columns
    new_column_name = request.GET.get("new_column_name")
    new_column_expression = request.GET.get("new_column_expression")
    if new_column_name and new_column_expression:
        df = df.withColumn(new_column_name, when(eval(new_column_expression), 1).otherwise(0))
    
    # store the dataframe in Azure SQL storage
    server_name = "<your-server-name>"
    database_name = "<your-database-name>"
    table_name = "<your-table-name>"
    user_name = "<your-username>"
    password = "<your-password>"
    
    driver= '{ODBC Driver 17 for SQL Server}'
    conn = pyodbc.connect(f"DRIVER={driver};SERVER={server_name};DATABASE={database_name};UID={user_name};PWD={password}")
    write_to_sql_server(df, table_name, conn)
    
    # convert the dataframe to an HTML table
    table_html = df.toPandas().to_html(index=False)
    
    # render the Django template with the HTML table and form inputs for renaming, filtering, and creating columns
    return render(request, "process_csv.html", {
        "table_html": table_html,
        "columns": df.columns,
        "column_map": column_map,
        "filter_col": filter_col,
        "filter_val": filter_val,
        "new_column_name": new_column_name,
        "new_column_expression": new_column_expression,
    })
