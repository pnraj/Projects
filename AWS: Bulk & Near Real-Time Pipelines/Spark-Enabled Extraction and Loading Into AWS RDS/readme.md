<div align="center"> <h1> SPARK-ENABLED EXTRACTION AND LOADING INTO AWS RDS </h1> </div>

<h3> Problem Statement:</h3>

1. To extract the data from [SEC.gov]("https://www.sec.gov/edgar/sec-api-documentation") (Zip) and stored in PySpark DataFrame. Each row in DataFrame will represent Each JSON file in the Zip and store the DataFrame into AWS S3 as Json file using Boto3
2. Get the File From AWS S3 using Boto3 and Transform the Data Suitable for AWS RDS Mysql Instance.

