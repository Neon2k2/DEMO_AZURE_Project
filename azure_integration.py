from pyspark.sql import SparkSession

# read CSV file from Azure Blob Storage into a dataframe
def read_csv_from_blob(blob_account_name, blob_account_access_key, container_name, file_path):
    spark = SparkSession.builder.appName("CSV to SQL").getOrCreate()
    spark.conf.set("fs.azure.account.key."+blob_account_name+".blob.core.windows.net",
                   blob_account_access_key)
    df = spark.read.format("csv").option("header", "true").load("wasbs://"+container_name+"@"+blob_account_name+".blob.core.windows.net/"+file_path)
    return df

# write dataframe to Azure SQL Database
def write_to_sql_server(df, server_name, database_name, table_name, username, password):
    jdbc_url = "jdbc:sqlserver://" + server_name + ".database.windows.net:1433;database=" + database_name + ";user=" + username + ";password=" + password
    df.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", table_name) \
        .option("user", username) \
        .option("password", password) \
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
        .mode("overwrite") \
        .save()
