import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('phonphe.db')

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