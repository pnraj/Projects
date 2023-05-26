# YouTube Data Harvesting and Warehousing:
  > Using Python, MYSQL, MongoDB, Streamlit and Googleapiclient

## Project Descriptions:

- The problem statement is to create a Streamlit application that allows users to access and analyze data from __Multiple YouTube Channels__:
   
   - Ability to input a _**YouTube channel ID**_ and retrieve all the relevant data using _**Google API**_.
  
        __| Channel name | Subscribers | Total video count | Playlist ID | Video ID | Likes| Comments of each video |__
     
   - Option to store the data in a MongoDB database as a data lake.
   - Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.
   - Option to select a channel name and migrate its data from the data lake to a SQL database as tables.
   - Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.

## How To Use The App: _[Click Here to Use Live App](https://pnraj-youtube-data-harvesting-and-warehousingyoutubeapi-9xleb8.streamlit.app/)_
<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/d90cf91e-1467-4fec-a7ab-5fdfad55f4c3" alt="YouTube API APP">
 </p>

1.__Single Channel Mode:__

  - Copy Your Desired YouTube Channel link 
      - Eg:  ` https://www.youtube.com/@realpython  or  https://www.youtube.com/channel/UCxvbui348912893489kj`
  - Paste Your Link In Text Box Next to DropDown And Press Enter
  - Wait For App To Make _API Request_ To **YouTube** And _Fetch Data_
  - You Have Three Options Available In Single Mode:
      - Basic Details of Channels Like  __Channel name,Subscribers,Total video count,Playlist ID,Video ID,Likes,Comments of each video__
      - Select Any Video From _Latest 100 Videos_ To View its Each Comments and Its Replies
      - Upload to MongoDB and MysqlDB and Options to View Data From **_Pre_Defined_ And _Custom Queries_** 
  
 2.__Multi Channel Mode:__
 
   - Enter Your Keyword of The Channel Name or Topic Covered In the Channel In Text Box Next to DropDown And Press Enter
      > _Top 10 in Result wil be Shown as Result_
   - Wait For App To Make _API Request_ To **YouTube** And _Fetch Data_
   - Same As Single Channel Mode But it Have Additional Options of **Selecting Channel Names** For uploading To _Mysql DataBase_
 
 ## Basic Requirements:

- __[Python 3.11](https://www.google.com/search?q=docs.python.org)__
- __[googleapiclient](https://www.google.com/search?q=googleapiclient+python)__ 
- __[mysql_connector](https://www.google.com/search?q=mysql+connector)__ 
- __[Pandas](https://www.google.com/search?q=python+pandas)__
- __[Streamlit](https://www.google.com/search?q=python+streamlit)__
- __[Numpy](https://www.google.com/search?q=numpy)__ 
- __[pymongo](https://www.google.com/search?q=pymongo)__
- __[requests](https://www.google.com/search?q=requests)__


<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/72ee83a0-501d-4fae-b474-bd42fb49e101" alt="Project WorkFlow">
 </p>

## General BackEnd WorkFlow Of This Project:
1.__Api Call And Data Sorting:__

  - _Based On The Users Need, Users Can Fetch Data From YouTube By Entering Url or Keyword_ 
  - To Make This Work I Designed Two Separate Files To Make Api Calls **_Single_Channel.py_** and **_Multi_Channel.py_** using **_Googleapiclient_**
      > which is inside off __Yapi__ Directory Of This Repo
  - After Data Got Fetched it is Shown as Three Separate Section Chanenl Details, Video Details, Comments Details
  - For Sorting And Isolation of Values From Data I have Used **_Pandas_** 
  - For Visualize The Data I Had Used **_Streamlit_** Inbuilt markdown features along with html 
  
2.__Uploading To MongoDb Atlas:__
    
  - Api call Gets Data in _JSON_ Format with lots of Details in each catagories:[Youtube Docs](https://developers.google.com/youtube/v3/docs/)
  
  ``` py
                    1. Channels
                    2. Videos 
                    3. CommentThreads
                    4. Search and many more
  ```
  
  - Data get Formated and Made Ready for Users to Upload to MongoDB which is **_Data Lake_** 
  - In MongoDB Each users Data is Stored in DB Called `youtube` and Collections name is Created based upon on the users Channel search
  - Sample of Data are shown to Users in **_Streamlit_** App After Succesfull Insert of Data into _[MongoDB Atlas](https://mongodb.com/)_

##### MongoDB Data Sample
  ``` json
  
                      {
           "_id":"ExamPro-Channel",
           "Channels_Data":[
              {
                 "Channel_id":"UC2EsmbKnDNE7y1N3nZYCuGw",
                 "Channel_Name":"ExamPro",
                 "Playlist_id":"UU2EsmbKnDNE7y1N3nZYCuGw",
                 "Created_Date":"2018-10-15T00:48:34Z",
                 "Subcribers":"27200",
                 "TotalViews":"3088251",
                 "TotalVideos":"2754",
                 "Thumbnail":"https://yt3.ggpht.com/Cp5qTPY5Riz_MkI-WgSShDIfddjKlO7NYpWu-uYABE7ghCHFuF2LGAPRovaJ8DNGxswIkWGv1Q=s240-c-k-c0x00ffffff-no-rj",
                 "Channel_link":"https://www.youtube.com/channel/UC2EsmbKnDNE7y1N3nZYCuGw"
              }
           ]
        }
  ```




3.__Uploading To Mysql DataBase:__

   - Data From MongoDB are then Converted into Tables and Rows using __Pandas__ with Normalization of Values are ready to Upload to MysqlDB
   - **_Mysql Connector_** is used for Connecting App and MysqlDB 
   - In Multiple Channel Mode Users Have Options of Choosing Channels That Needs to Be Uploaded to MysqlDB
   - MysqlDB will have Three Tables **_Channel_Table, Videos_Table, Comments_Table_** 
   
   ``` sql
           
        CREATE TABLE IF NOT EXISTS Channel_Table (
            Ch_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Channel_Id VARCHAR(30) UNIQUE,
            Channel_Name VARCHAR(40),
            Playlist_Id VARCHAR(30),
            Created_Date DATETIME,
            Subscribers BIGINT,
            Total_Views BIGINT,
            Total_Videos BIGINT);
     
        CREATE TABLE IF NOT EXISTS Videos_Table (
            Vid_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Channel_Id INTEGER,
            Video_Id VARCHAR(20),
            Video_Title VARCHAR(100),
            Uploaded_Date DATETIME,
            Total_Views BIGINT,
            Total_Likes BIGINT,
            Total_Comments BIGINT,
            FOREIGN KEY (Channel_Id) REFERENCES Channel_Table (Ch_id));
    
        CREATE TABLE IF NOT EXISTS Comments_Table (
            Com_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Channel_Id INTEGER,
            Video_Id INTEGER,
            Video_Title VARCHAR(100),
            Comments VARCHAR(200),
            Replies VARCHAR(200),
            FOREIGN KEY (Channel_Id) REFERENCES Channel_Table (Ch_id),
            FOREIGN KEY (Video_Id) REFERENCES Videos_Table (Vid_id));
   ```
   
   
   
   
   <p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/4be53ef8-3089-468d-af69-1a201c9c5220" alt="MysqlDB Schema">
 </p>
  


4.__Querying From Mysql DataBase:__

   - Querying Data From MysqlDB Have Two Options With **_Pre-Defined Query_** and **_Custom Query_**
   - **_Pre-Defined Query_** will display details of the Selected Channels or Channels that are currentely Shown in Channels List 
   - **_Custom Query_** will have options to use **_SQL_** Queries to get Details of all Channels, Videos, Comments Using all basic _SQL_ Commends like **_JOIN,WHERE,SELECT,GROUP BY, HAVING_**  

``` sql

        SELECT a.Channel_Name,b.Video_Title,b.Total_Likes 
            FROM Channel_Table  a JOIN Videos_Table b ON 
                a.Ch_id = b.Channel_Id WHERE b.Total_Likes > 20;

```
