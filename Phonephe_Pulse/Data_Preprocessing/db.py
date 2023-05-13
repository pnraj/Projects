## Use this file to connect to database to query your data and covert it the dataframe
import pandas as pd
import mysql.connector as mysql


conn = mysql.connect(host='localhost',user='root',password='',port=3307)
cur = conn.cursor()
cur.execute("use phonephe ")

user = ("SELECT s.`StateName`, ul.`DistrictName`, ul.`UsersCount`, ul.`AppOpening`,ul.`Quarter`, y.`Year`   \
FROM `userslocation` AS ul \
INNER JOIN `year` AS y \
ON ul.`YearID` = y.`YearID` \
CROSS JOIN `state` AS s \
ON ul.`StateID` = s.`StateID`")

trans = ("SELECT s.`StateName`, tl.`DistrictName`, tl.`TotalTransactionCount`, tl.`TotalTransactionAmount`,tl.`Quarter`, y.`Year`   \
FROM `TransactionLocation` AS tl \
INNER JOIN `year` AS y \
ON tl.`YearID` = y.`YearID` \
CROSS JOIN `state` AS s \
ON tl.`StateID` = s.`StateID`")

pin = ("SELECT s.`StateName`, pl.`Pincode`, pl.`Total_Registered_users`,pl.`Quarter`, y.`Year`   \
FROM `Pincodes` AS pl \
INNER JOIN `year` AS y \
ON pl.`YearID` = y.`YearID` \
CROSS JOIN `state` AS s \
ON pl.`StateID` = s.`StateID`")

pay = ("SELECT s.`StateName`, tl.`TransactionMethod`, tl.`TransactionCounts`, tl.`TransactionAmounts`,tl.`Quarter`, y.`Year`   \
FROM `TransactionMethods` AS tl \
INNER JOIN `year` AS y \
ON tl.`YearID` = y.`YearID` \
CROSS JOIN `state` AS s \
ON tl.`StateID` = s.`StateID`")


queries = [user, trans, pin,pay]
def data_fetch(queries):
    dfs = []
    for i, query in enumerate(queries):
        cur.execute(query)
        data = cur.fetchall()
        column_names = [i[0] for i in cur.description]
        df = pd.DataFrame(data, columns=column_names)
        dfs.append(df)
    return dfs


#users_df,trans_df,pin_df,pay_df = data_fetch(queries)

