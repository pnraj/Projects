<div align="center"> <h1> SPARK-ENABLED EXTRACTION AND LOADING INTO AWS RDS </h1> </div>
<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/f6e07a28-dce6-4fb2-8795-ddb8f46b16b8" alt="Project WorkFlow" width="990" height="650">
 </p>

<h3>Requirments:</h3>

- Python<=3.10
- `Apache Spark 3`
- boto3
- requests
- _**DataBricks**_ Account (minimum community Edition) and basics about _**Pyspark**_
- Basics about _**AWS services**_ and to Create `S3 bucket` & `RDS mysql instance`

<h3> Problem Statement:</h3>

1. To extract the data from [SEC.gov](https://www.sec.gov/edgar/sec-api-documentation) (submissions.zip) and stored in _**PySpark DataFrame**_. Each **`Row`** in DataFrame will represent Each _**JSON**_ file in the Zip and store the DataFrame into _**AWS S3**_ as Json file using Boto3
2. Get the File From _**AWS S3**_ using _Boto3_ and Transform the Data Suitable for _**AWS RDS**_ _Mysql_ Instance.

<h3>PART 1:</h3> 

Import DataBricks From here: [Part 1](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/5104685777254537/1422103546938979/2720986376738102/latest.html)

1. Download _Zip_ File From SEC.gov Using _**requests**_ lib and Extract the files
```py
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',"Accept": "application/zip"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        zip_file = io.BytesIO(response.content)
        if zip_file:
            with zipfile.ZipFile(zip_file, 'a') as zip_ref:
                zip_ref.extractall(extract_path)
```

2. Convert the Extracted json files to _Pyspark DataFrame_ and Each DataFrame _Row_ Represents Each _Json_ File.
```py
    jdf = spark.read.json("file://" + extract_path + "*.json")
    print("Spark DataFrame Created Successfully")
    if jdf:
        # converting the json dataframe into json files 
        jdf.coalesce(5).write.json("file://" + DfJson_Path) # Defining Number of json files as "5"
        print("Json Files are Created from Spark DataFrame")
```

3. Convert the _Pyspark DataFrame_ into Json using Pyspark Write method and Save into _`AWS S3`_(After Compressing Into Zip)
```py
    s3 = boto3.resource('s3', aws_access_key_id = api_key, aws_secret_access_key=api_secret)
    # Upload the file to S3
    s3.Object(s3_bucket_name, s3_key).upload_file(s3_Zip_Path)
```

<h3>PART 2:</h3> 

Import DataBricks From here: [Part 2](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/5104685777254537/1422103546938968/2720986376738102/latest.html)

1. Download the Compressed Json File from **`AWS S3`** and Uncompress it.
```py
    s3_resource = boto3.resource('s3', aws_access_key_id = api_key, aws_secret_access_key = api_secret)
    # Download the file from S3
    s3_resource.Object(s3_bucket_name, s3_key).download_file(s3_Zip_Path)
    subprocess.check_call(f"unzip {s3_Zip_Path} -d {unzip_dir}", shell=True)
    print("Unzipped successfully!")
```

2. Convert the Json file into _`Pyspark DataFrame`_ and  Segregate the desired part of the data
```py
    jdf = spark.read.json("file:///tmp/S3_SEC_Files/*.json")

    # Dropping the Empty Collumns in DataSet
    need_col = ['name', 'ein', 'cik', 'stateOfIncorporation', 'addresses', 'phone', 'filings']
    del_col = [col_name for col_name in jdf.columns if col_name not in need_col]
    
    jdf = jdf.drop(*del_col)
```

3. SEC Data Contains Details about `Company`, Company `Address` and `Form` Filled By Company
<h5>Company DataFrame</h5>

```py
    company_table = company_table.select(col("_1").alias("Company_Name"),
                    col("_2").alias("Employer_Identification_Number").cast(IntegerType()),
                    col("_3").alias("SEC_Central_Index_Key").cast(IntegerType()),
                    col("_4").alias("Registered_State"),
                    col("_5").alias("Phone_Number"), col("_6").alias("index").cast(IntegerType()))
```
<h5>Contact DataFrame</h5>

```py
    mailing_df = mailing_df.select(col('_1').alias('City'),col('_2').alias('State'),
                               col('_3').alias('Zipcode').cast(IntegerType()),col('_4').alias('Address'),
                               col('_5').alias('index').cast(IntegerType()))
    address_df = mailing_df.join(company_table.select(col('Phone_Number'), col('index')),on='index',how='left')
    clean_phone_number_udf = udf(clean_phone_number)
    contact_table = address_df.withColumn("Phone_Number", clean_phone_number_udf(col("Phone_Number"))) \
                               .withColumn("Phone_Number", col("Phone_Number").cast(IntegerType()))
    contact_table = contact_table.select('Address', 'Phone_Number', 'City', 'State', 'ZipCode', col('index').alias('company_index'))
``` 
<h5>Form DataFrame</h5>

```py
    filling_df1 = filling_df1.select(col('_1').alias('accessionNumber'),col('_2').alias('filingDate'),
                                 col('_3').alias('acceptanceDateTime'),col('_4').alias('act'),
                                 col('_5').alias('form'),col('_6').alias('fileNumber'),
                                 col('_7').alias('filmNumber'),col('_8').alias('size'), col('_9').alias('index').cast(IntegerType()))
```

4. Data can be Transformed into Three Tables and inserted into  AWS RDS<table schema >
<p>
    <img src="https://github.com/pnraj/Projects/assets/29162796/ee88ed74-dce4-4ebd-af78-f461b091aec5" alt="Table Schema" width="990" height="550">
</p>

**Company Table have Five Columns:**
   
   | Company_index | Company_Name | Employer_Identification_Number| SEC_Central_Index_Key| Registered_State |
   |---------------|--------------|-------------------------------|----------------------|------------------|

```sql

     CREATE TABLE IF NOT EXISTS `Company_Table`(
    `Company_index` INT PRIMARY KEY,
    `Company_Name` VARCHAR(200),
    `Employer_Identification_Number` INT,
    `SEC_Central_Index_Key` INT,
    `Registered_State` VARCHAR(10));
```

**Contacts Table have Six Columns:**

   | company_index | Address | Phone_Number | City | State | ZipCode| 
   |---------------|---------|--------------|------|-------|--------|

```sql

    CREATE TABLE IF NOT EXISTS Contact_Table (
    `Company_index` int PRIMARY KEY, `Address` varchar(230), `Phone_Number` int, `City` varchar(20),
    `State` varchar(5), `ZipCode` int,
    foreign key (`Company_index`) references Company_Table (Company_index)
    );
```


**Form Table have Nine Columns:**

   | Company_index | Acession_Number| Filling_Date | Acceptance_DateTime| Act | Form | File_Number| Film_Number | Size |
   |---------------|----------------|--------------|--------------------|-----|------|------------|-------------|------|

```sql

    CREATE TABLE IF NOT EXISTS Form_table(
    Company_index int PRIMARY KEY,
    Acession_Number varchar(30),
    Filling_Date date,
    Acceptance_DateTime timestamp,
    Act int,
    Form varchar(20),
    File_Number varchar(40),
    Film_Number int,
    `Size` int,
    foreign key (Company_index) references Company_Table (Company_index)
    );
```

<h5>Load Into AWS RDS Using Pyspark write method and JDBC Connection(Parallelism support)</h5>

```py
    def jdbc_conn(host, user, password, dbname): 
      jdbc_url = f"jdbc:mysql://{host}:3306/{dbname}"
      connection_properties = {"user": f"{user}", "password": f"{password}"}
      return jdbc_url, connection_properties
```

```py
    def sparkToRds(df,sample_table,jdbc_url,connection_properties):
      try:
          # Write the DataFrame to a table in the MySQL database
          df.write \
              .format("jdbc") \
              .option("url", jdbc_url) \
              .option("dbtable", f"{sample_table}") \
              .option("user", connection_properties["user"]) \
              .option("password", connection_properties["password"]) \
              .mode("append") \
              .save()
  
          print(f"successfully Inserted Into AWS RDS SEC DATABASE: {sample_table}.")
  
      except Exception as e:
          print(f"Connection failed: {str(e)}")
```



