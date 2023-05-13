#this is Sql_queries.py


State_table = ("CREATE TABLE IF NOT EXISTS State (StateID INT AUTO_INCREMENT PRIMARY KEY,StateName VARCHAR(255) NOT NULL)")

Year_table = ("CREATE TABLE IF NOT EXISTS Year (YearID INT AUTO_INCREMENT PRIMARY KEY,Year INT NOT NULL)")

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

Users_Location = ("CREATE TABLE IF NOT EXISTS UsersLocation ("
"`UserLocationID` INT AUTO_INCREMENT PRIMARY KEY,"
"`DistrictName` VARCHAR(255) NOT NULL,"
"`UsersCount` INT NOT NULL,"
"`AppOpening` DECIMAL(10, 2) NOT NULL,"
"`Quarter` INT NOT NULL,"                  
"`StateID` INT NOT NULL,"
"`YearID` INT NOT NULL,"
"FOREIGN KEY (`StateID`) REFERENCES State(`StateID`),"
"FOREIGN KEY (`YearID`) REFERENCES Year(`YearID`))")

Trans_Location = ("CREATE TABLE IF NOT EXISTS TransactionLocation ("
"`TransactionLocationID` INT AUTO_INCREMENT PRIMARY KEY,"
"`DistrictName` VARCHAR(255) NOT NULL,"
"`TotalTransactionCount` INT NOT NULL,"
"`TotalTransactionAmount` FLOAT NOT NULL,"
"`Quarter` INT NOT NULL,"
"`StateID` INT NOT NULL,"
"`YearID` INT NOT NULL,"
"FOREIGN KEY (`StateID`) REFERENCES State(`StateID`),"
"FOREIGN KEY (`YearID`) REFERENCES Year(`YearID`))")


Trans_Methods = ("CREATE TABLE IF NOT EXISTS TransactionMethods ("
"`TransactionMethodID` INT AUTO_INCREMENT PRIMARY KEY,"
"`TransactionMethod` VARCHAR(255) NOT NULL,"
"`TransactionCounts` INT NOT NULL,"
"`TransactionAmounts` FLOAT NOT NULL,"
"`Quarter` INT NOT NULL,"
"`StateID` INT NOT NULL,"
"`YearID` INT NOT NULL,"
"FOREIGN KEY (`StateID`) REFERENCES State(`StateID`),"
"FOREIGN KEY (`YearID`) REFERENCES Year(`YearID`))")

Pincode_table = ("CREATE TABLE IF NOT EXISTS Pincodes ("
"`PincodeID` INT AUTO_INCREMENT PRIMARY KEY,"
"`Pincodes` INT NOT NULL,"
"`Total_Registered_users` INT NOT NULL,"
"`Quarter` INT NOT NULL,"
"`StateID` INT NOT NULL,"
"`YearID` INT NOT NULL,"
"FOREIGN KEY (`StateID`) REFERENCES State(`StateID`),"
"FOREIGN KEY (`YearID`) REFERENCES Year(`YearID`))")


#Pincodes	Total_Registered_users	state	year	quater
queries = [State_table,Year_table,Users_Device,Users_Location,Trans_Location,Trans_Methods,Pincode_table]