from pyspark.sql.functions import col, concat, struct, udf, posexplode_outer, to_date, when
from pyspark.sql.types import *
from pyspark.sql import Row
import boto3, subprocess, re, datetime, os
from dotenv import load_dotenv


# importing df function from sub files
from company_df import Company_table
from contact_df import contacts_df, contact_table
from form_df import sec_fillings_df, form_table

#
def GetS3Data(api_key,api_secret,s3_key,s3_bucket_name,s3_Zip_Path,unzip_dir):
    try:
        # Initialize the S3 resource
        s3_resource = boto3.resource('s3', aws_access_key_id = api_key, aws_secret_access_key = api_secret)
        # Download the file from S3
        s3_resource.Object(s3_bucket_name, s3_key).download_file(s3_Zip_Path)
        print("File downloaded successfully from S3.")
        subprocess.check_call(f"unzip {s3_Zip_Path} -d {unzip_dir}", shell=True)
        print("Unzipped successfully!")

    except Exception as e:
        print(f"Unzip Error: {e}")        


def JsonToDataFrame(unzip_dir):
    # spark should be created using SparkSession 
    jdf = spark.read.json(f"file://{unzip_dir}*.json")

    # Dropping the Empty Collumns in DataSet
    need_col = ['name', 'ein', 'cik', 'stateOfIncorporation', 'addresses', 'phone', 'filings']
    del_col = [col_name for col_name in jdf.columns if col_name not in need_col]

    jdf = jdf.drop(*del_col)
    return jdf

def df_main(api_key,api_secret,s3_key,s3_bucket_name,s3_Zip_Path,unzip_dir):
    #Execution Starts here
    GetS3Data(api_key,api_secret,s3_key,s3_bucket_name,s3_Zip_Path,unzip_dir)
    jdf = JsonToDataFrame(unzip_dir)
    #Company_table
    com_df, company_table = Company_table(jdf)
    #contact_table
    mailing_df = contacts_df(jdf)
    cont_df = contact_table(mailing_df,company_table)
    #form_table
    filling_df1 = sec_fillings_df(jdf)
    rds_df = form_table(filling_df1)

    return com_df, cont_df, rds_df



    
