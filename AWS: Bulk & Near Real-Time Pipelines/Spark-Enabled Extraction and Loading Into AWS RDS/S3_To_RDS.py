import os
from dotenv import load_dotenv
load_dotenv()
from df_files.S3_To_DF import df_main

def jdbc_conn(host, user, password, dbname):
    # Configure the MySQL JDBC connection properties
    jdbc_url = f"jdbc:mysql://{host}:3306/{dbname}"
    connection_properties = {
        "user": f"{user}",
        "password": f"{password}"
    }
    return jdbc_url, connection_properties


def sparkToRds(df,sample_table,jdbc_url,connection_properties):
    try:
        # Write the DataFrame to a temporary table in the MySQL database
        df.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", f"{sample_table}") \
            .option("user", connection_properties["user"]) \
            .option("password", connection_properties["password"]) \
            .mode("append") \
            .save()

        # If the code reaches this point without raising an exception, the connection is successful
        print(f"successfully Inserted Into AWS RDS SEC DATABASE: {sample_table}.")

    except Exception as e:
        print(f"Connection failed: {str(e)}")

def load_to_rds(rds_df,cont_df,com_df,jdbc_url,connection_properties):
    try:

        df_table = {"Company_Table": com_df, "Contact_Table": cont_df ,"Form_table": rds_df}
        for table, df in df_table.items():
            sparkToRds(df, table, jdbc_url, connection_properties)

    except Exception as e:
        print(str(e))

def main_rds(api_key,api_secret,s3_key,s3_bucket_name,s3_Zip_Path,unzip_dir,host, user, password, dbname):
  
        
    com_df, cont_df, rds_df = df_main(api_key,api_secret,s3_key,s3_bucket_name,s3_Zip_Path,unzip_dir)

    jdbc_url, connection_properties = jdbc_conn(host, user, password, dbname)

    load_to_rds(rds_df,cont_df,com_df,jdbc_url,connection_properties)


if __name__ == "__main__":
    
    # Set your AWS credentials
    api_key, api_secret = os.getenv('api_key'), os.getenv('api_secrets')
    # Set the S3 bucket name and key (path of the file in the bucket)
    s3_bucket_name, s3_key = 'guvi-sec-json-data', 'sec_json.zip'
    # Specify the local file path to save the downloaded file
    s3_Zip_Path, unzip_dir = '/tmp/sec_json.zip', "/tmp/S3_SEC_Files/"   

    host, user, password, dbname = os.getenv('host'), os.getenv('user'), os.getenv('password'), os.getenv('dbname') 

    main_rds(api_key,api_secret,s3_key,s3_bucket_name,s3_Zip_Path,unzip_dir,host, user, password, dbname)