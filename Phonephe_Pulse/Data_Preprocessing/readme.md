## This Directory Explains The Processing Of `Raw` Data And Convert Into `Structured` Data

### Requirment for Processing the data

1. Python==3.11
2. Pandas>=3.7
3. Mysql.connector
4. Os(python inbuilt)
5. Pathlib(python inbuilt)

### How To Processes The Phonepe Github Data Using Files In This Directory

1. First is Optional but I decided to include it anyway `git_clone.py` is used for cloning the Github public repo by running it as `script`
```py
      def get_file():
          url = 'https://github.com/PhonePe/pulse/archive/refs/heads/master.zip'
          response = requests.get(url)
```

2. `Extract.py` where we start the processing the unstructered data and converting them into structured data using `Pandas DataFrame`
```py
      class agg_tran:
          def __init__(self, agg_tran_path):
              self.state_aggregated_transaction = pd.DataFrame({})
              self.agg_tran_path = agg_tran_path
          def aggregated_transaction(self,state, year, quarter, path):
              a_dft = pd.read_json(path) # dataframe
              # data sorting
              trs_df = a_dft.data.transactionData
              if trs_df:
                  for i in trs_df:
                      all_rows = {"Transaction_method":i['name'],"Transaction_Counts":i['paymentInstruments'][0]['count'],"Transaction_amounts":i['paymentInstruments'][0]['amount'],"state":state,"year":year,"quarter":quarter}
                      all_rows_df = pd.DataFrame.from_dict([all_rows])
                      self.state_aggregated_transaction = pd.concat([self.state_aggregated_transaction,all_rows_df])
                      self.state_aggregated_transaction['Transaction_amounts'] = self.state_aggregated_transaction['Transaction_amounts'].apply(lambda x: int(x))
                  self.state_aggregated_transaction.reset_index(drop=True, inplace=True)
          def extract_data(self):
                  for state in os.listdir(self.agg_tran_path):
                      state_path = os.path.join(self.agg_tran_path, state)
                      for year in range(2018, 2023):
                          year_path = os.path.join(state_path, str(year))
                          qfiles = []
                          for (dirpath, dirnames, filenames) in os.walk(year_path):
                              qfiles.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.json')])
                              break
                          for qfile_path in qfiles:
                              quarter = Path(qfile_path).stem
                              self.aggregated_transaction(state, year, quarter, qfile_path)
                  return self.state_aggregated_transaction
```
> If You Need Extracted data in `csv` format, you can run `Extract.py` alone and convert them using pandas to csv function `pd.to_csv()`
> ``` By calling the function all_df(path/where/files/are/stored)``` 

3. `Sql_queries.py` contains file where mysql queries, that are neede for inserting the data into Mysql database
```py
        Users_Device = ("CREATE TABLE IF NOT EXISTS UsersDevice ("
          "`UsersDeviceID` INT AUTO_INCREMENT PRIMARY KEY,"
          "`DeviceBrandName` VARCHAR(255) NOT NULL,"
          "`BrandCount` INT NOT NULL,"
          "`Percentage` FLOAT NOT NULL,"
          "`NoOfUsers` INT NOT NULL,"
          "`AppOpening` DECIMAL(10, 2) NOT NULL,"
          "`Quarter` INT NOT NULL,"                
          "`StateID` INT NOT NULL,"
          "`YearID` INT NOT NULL,"
          "FOREIGN KEY (`StateID`) REFERENCES State(`StateID`),"
          "FOREIGN KEY (`YearID`) REFERENCES Year(`YearID`))")
```
> Feel free to edit the database,tables,columns names as you wish
4. After converting the data into `Pandas DataFrame` we are inseting the data into mysql Database using `mysql.connector` python lib by running `Load.py`
```py
        def all_data():
            conn,cursor = mydb(user='root', password='', host=' DESKTOP-BT6FLH7', port=3307) #airflow to local
            create_tables(conn,cursor)
            Trans_Methods_insert(conn,cursor)
            Trans_Location_insert(conn,cursor)
            Users_Location_insert(conn,cursor)
            Users_Device_insert(conn,cursor)
            Pincode_insert(conn,cursor)
            cursor.close()
            conn.close() #close database connection
```
> For ease of use, I have created `Load.py` fully functional meaning, all you have to do is just run `Load.py` alone and python will take care of processing
