# Data Engineering Projects:

## Project Description
This repository Contains collection of resources and code for the aspiring data engineer. It aims to provide a solid foundation and practical guidance for individuals interested in pursuing a career in the field of data engineering.

<h3 align="left">PROJECTS</h3>

[API TO RDS USING LAMBDA WITH SLACK ERROR MONITORING](https://github.com/pnraj/Projects/tree/master/AWS%3A%20Bulk%20%26%20Near%20Real-Time%20Pipelines/API%20TO%20RDS%20USING%20LAMBDA%20WITH%20SLACK%20ERROR%20MONITORING)

<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/fe89c91f-a1ab-46e9-b589-4e9ef1bafa5a" alt="Project WorkFlow" width="690" height="390">
</p>

- Using _**AWS Lambda**_ Api is fetched from a link, processed and load into _**AWS RDS**_ with **15 seconds** Interval
- Two Lambda functions are used in these Pipeline where **First lambda** will be invoked by **Aws Step-Function** which is invoked by **Cloudwatch / EventBridge Rules**. For Every _One minute_ until the Rule gets disabled.
- **Second Lambda** Function is used to fetch Api and Loaded into AWS RDS.
- **Aws Step-Function** is Working Based _ASL(Amazon State Language)_ which is based on _Json_ file Structure
- If any _error or Database connction_ problem occurs notification is sent to **slack channel** using _slack_sdk_
- All internal Connections between AWS services are based on _**IAM Role and Policies**_.

[SPARK-ENABLED EXTRACTION AND LOADING INTO AWS RDS](https://github.com/pnraj/Projects/tree/master/AWS%3A%20Bulk%20%26%20Near%20Real-Time%20Pipelines/Spark-Enabled%20Extraction%20and%20Loading%20Into%20AWS%20RDS)

<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/f6e07a28-dce6-4fb2-8795-ddb8f46b16b8" alt="Project WorkFlow" width="690" height="390">
 </p>
 
- There are **Two Part** in these Project.\n
- **Part1** is Getting Data from **SEC.gov**(**Zip** format) contains more than _8.5 lakh_ **Json files** around **6gb** after _uncompressing_.
- By Using _**Apache Spark(PySpark)**_ and _DataBricks_, Json files are converted into **Pyspark DataFrames** with _Each_ json File representing _single row_ in DataFrame.The _DataFrame_ is later converted into _Json file_ and uploaded into **AWS S3**.
- **Part2** is Getting Data from AWS S3, Do the Needed Transformation and upload into _**AWS RDS-Mysql Instance**_
- The Data From S3 is Converted into _PySpark DataFrame_ and Isolate needed Columns that needed to uplaoded into RDS
- Important Function Used for Transformation are _**join, posexplode_outer, udf, concat, to_date, struct and Row.**_

[YouTube Data Harvesting and Warehousing](https://github.com/pnraj/Projects/tree/master/YouTube_Data_Harvesting_and_Warehousing)

<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/72ee83a0-501d-4fae-b474-bd42fb49e101" alt="Project WorkFlow" width="690" height="390">
 </p>


- Ability to input a **YouTube channel ID** and retrieve all the relevant data using **Google API**.
- Option to store the data in a **MongoDB database** as a _Data Lake_.
- Ability to collect data for up to 10 different YouTube channels and store them in the data lake based upon user Requirment.
- Option to select a _channel name_ and migrate its data from the data lake to a **Mysql(SQL) Database** as tables.
- Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.

[PhonePe Pulse Data Analysis 2018-2022](https://github.com/pnraj/Projects/tree/master/Phonephe_Pulse)

<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/b97ce7b9-634a-4612-bef7-77369b4a89c6" alt="Phonepe" width="690" height="390">
</p>

- Getting the _**PhonePe Payment App-Data**_ in **Json format** from **Github** repo 
- The _Json files_ are separated for every _**3 Month / 1 Quarter**_ of years from **2018-2022** for every _states and districts_ in **India**.
- Using _Python_ **os module**, Pipeline is Built to **Iterate** to each folder and get data from _json file_ and convert into _**pandas DataFrame**_.
- Json Files Contains Details about _**Amount of Transactions**_ and _**Transaction Location**_ where Users Do that Transaction.
- Using The DataFrame, **Visualization** are made using **Plotly and Streamlit** on _Geo, Bar, line, Pie, Area_ chart are included.

[Twitter Scraping](https://github.com/pnraj/Twitter_scraping)

<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/0266df32-e6db-4f80-b5a2-83da20db0c45" alt="Twitter scaping" width="690" height="390">
</p>

- Based on User needs **Twitter** _Tweets_ are **Extracted and Uploaded** into **Mongodb** using UI based upon **Streamlite** based app
- Users have to enter **Tweets topic or hashtag**, **Starting Date**, **Ending Date**, **Total Number of Tweets** needed to extracted in app and 
- App will _fetch_ the data by using **Snscrape** and convert the data into **Pandas DataFrame** and displayed as _Tabular Format_.
- After Checking the data users can have options to download the data as _**json**_, _**csv**_ or can be _**uploaded into Mongodb**_.


## License
This project is licensed under the [MIT License](LICENSE). Please review the license file for more details.

## Contact
If you have any questions or suggestions regarding this project, feel free to reach out to me at [pnrajk@gmail.com](mailto:pnrajk@gmail.com).
