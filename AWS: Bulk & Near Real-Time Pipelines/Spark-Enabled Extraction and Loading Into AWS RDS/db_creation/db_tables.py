import os, mysql.connector
from dotenv import load_dotenv

# Load environment variables from file
def mysql_db_tables(host,user,port,password):
  
  conn = mysql.connector.connect(
      host=host,
      port=port,
      user=user,
      password=password
  )
  cur = conn.cursor()
  return conn,cur


sql_schema = [
'''CREATE TABLE IF NOT EXISTS `Company_Table` (
  `Company_index` INT PRIMARY KEY,
  `Company_Name` VARCHAR(200),
  `Employer_Identification_Number` INT,
  `SEC_Central_Index_Key` INT,
  `Registered_State` VARCHAR(10)
)''',

'''CREATE TABLE IF NOT EXISTS Contact_Table (
`Company_index` int PRIMARY KEY, `Address` varchar(230), `Phone_Number` int, `City` varchar(20),
`State` varchar(5), `ZipCode` int,
foreign key (`Company_index`) references Company_Table (Company_index)
)''',


'''CREATE TABLE IF NOT EXISTS Form_table(
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
)'''

]

def crete_tables(host,user,port,password,sql_schema):
  conn,cur = mysql_db_tables(host,user,port,password)
  cur.execute("create database if not exists secdb")
  cur.execute("use secdb")
  for schema in sql_schema:    
    cur.execute(schema)
    conn.commit()
  
  conn.close()

if __name__ == "__main__":
    load_dotenv()
    host,user,port,password = os.getenv("host"), os.getenv("user"), int(os.getenv("port")), os.getenv("password")
    crete_tables(host,user,port,password,sql_schema)
  