import os, io, zipfile, requests, boto3, subprocess
from dotenv import load_dotenv


def Get_SecData(url,extract_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',"Accept": "application/zip"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            zip_file = io.BytesIO(response.content)
            if zip_file:
                with zipfile.ZipFile(zip_file, 'a') as zip_ref:
                    zip_ref.extractall(extract_path)
                print("Zip file extracted successfully.")
        else:
            print("Failed to download the file:", response.status_code)

    except Exception as e:
        print("An error occurred in Get_SecData:", str(e))


def Json_to_SparkJson(DfJson_Path,extract_path):
    try:

        #reading json file from extracted location
        jdf = spark.read.json("file://" + extract_path + "*.json")
        print("Spark DataFrame Created Successfully")
        if jdf:
            # converting the json dataframe into json files 
            jdf.coalesce(5).write.json("file://" + DfJson_Path) # Defining Number of json files as "5"
            print("Json Files are Created from Spark DataFrame")

    except Exception as e:
        print("An error occurred in Json_to_SparkJson:", str(e))


def s3_file_upload(s3_Zip_Path,api_key,api_secret,s3_bucket_name,s3_key):
    # Initialize the S3
    try:
        s3 = boto3.resource('s3', aws_access_key_id = api_key, aws_secret_access_key=api_secret)
        # Upload the file to S3
        s3.Object(s3_bucket_name, s3_key).upload_file(s3_Zip_Path)
        print("File uploaded successfully to S3.")
    except Exception as e:
        print("An error occurred in s3_file_upload:", str(e))


def S3_Zip_Upload(DfJson_Path,s3_Zip_Path,api_key,api_secret,s3_bucket_name,s3_key):
    try:
        # files are Compressed for Uploading into S3
        subprocess.check_call(f"cd {DfJson_Path} && zip -j {s3_Zip_Path} *", shell=True)
        print("Compressed successfully!")
        # Files are Uploaded into S3
        s3_file_upload(s3_Zip_Path,api_key,api_secret,s3_bucket_name,s3_key)
        print("Zip Successfully Uploaded into S3")

    except Exception as e:
        print("An error occurred in S3_Zip_Upload:", str(e))

def SEC_To_S3(url,extract_path,DfJson_Path,s3_Zip_Path,api_key,api_secret,s3_bucket_name,s3_key):
    try:
        Get_SecData(url,extract_path)
        # Converting the Json Files into DataFrame and then Convert into Json(Each Files Represent Each Row in DataFrame)
        Json_to_SparkJson(DfJson_Path,extract_path)
        # Uploading the files into Aws S3            
        S3_Zip_Upload(DfJson_Path,s3_Zip_Path,api_key,api_secret,s3_bucket_name,s3_key)

        
    except Exception as e:
        print("An error occurred in SEC_To_S3:", str(e))

if __name__ == "__main__":
    load_dotenv()
    
    url = "https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip"
    extract_path = "/tmp/extracted/" 
    DfJson_Path = "/tmp/sec_json_files/"
    s3_Zip_Path = "/tmp/sec_json.zip"

    # Set your AWS credentials
    api_key = os.getenv('api_key')
    api_secret = os.getenv('api_secrets')

    # Set the S3 bucket name and key (destination path within the bucket)
    s3_bucket_name = 'guvi-sec-json-data'
    s3_key = 'sec_json.zip'

    
    SEC_To_S3(url,extract_path,DfJson_Path,s3_Zip_Path,api_key,api_secret,s3_bucket_name,s3_key)