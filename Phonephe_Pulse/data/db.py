import pandas as pd
import sqlite3
import wget

url = 'https://raw.githubusercontent.com/pnraj/Projects/master/Phonephe_Pulse/data/phonphe.db'
db_file = wget.download(url)

# Connect to the SQLite database
conn = sqlite3.connect(db_file)

# Query the tables and retrieve the results
users_query = "SELECT * FROM users;"
trans_query = "SELECT * FROM transactions;"
pin_query = "SELECT * FROM pins;"
pay_query = "SELECT * FROM payments;"

users_df = pd.read_sql_query(users_query, conn)
trans_df = pd.read_sql_query(trans_query, conn)
pin_df = pd.read_sql_query(pin_query, conn)
pay_df = pd.read_sql_query(pay_query, conn)

# Close the connection
conn.close()
