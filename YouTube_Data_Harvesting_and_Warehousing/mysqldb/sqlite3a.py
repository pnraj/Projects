import sqlite3
import pandas as pd
import wget


def mysql_insert(channel_df, video_df, comment_df):
    # Connect to the SQLite database
    url = "https://raw.githubusercontent.com/pnraj/Projects/master/YouTube_Data_Harvesting_and_Warehousing/mysqldb/YouTubeApi.db"
    db_file = wget.download(url)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    ch_schema = """
        CREATE TABLE IF NOT EXISTS Channel_Table (
            Ch_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Channel_Id VARCHAR(30) UNIQUE,
            Channel_Name VARCHAR(40),
            Playlist_Id VARCHAR(30),
            Created_Date DATETIME,
            Subscribers BIGINT,
            Total_Views BIGINT,
            Total_Videos BIGINT
        )
    """

    vi_schema = """
        CREATE TABLE IF NOT EXISTS Videos_Table (
            Vid_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Channel_Id INTEGER,
            Video_Id VARCHAR(20),
            Video_Title VARCHAR(100),
            Uploaded_Date DATETIME,
            Total_Views BIGINT,
            Total_Likes BIGINT,
            Total_Comments BIGINT,
            FOREIGN KEY (Channel_Id) REFERENCES Channel_Table (Ch_id)
        )
    """

    comm_schema = """
        CREATE TABLE IF NOT EXISTS Comments_Table (
            Com_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Channel_Id INTEGER,
            Video_Id INTEGER,
            Video_Title VARCHAR(100),
            Comments VARCHAR(200),
            Replies VARCHAR(200),
            FOREIGN KEY (Channel_Id) REFERENCES Channel_Table (Ch_id),
            FOREIGN KEY (Video_Id) REFERENCES Videos_Table (Vid_id)
        )
    """

    conn.execute("PRAGMA foreign_keys = 1")  # Enable foreign key support

    conn.execute(ch_schema)
    conn.execute(vi_schema)
    conn.execute(comm_schema)

    for index, row in channel_df.iterrows():
        # Check if Channel_Id already exists in Channel_Table
        cursor.execute("SELECT Channel_Id FROM Channel_Table WHERE Channel_Id=?", (row['Channel_id'],))
        existing_channel = cursor.fetchone()

        if not existing_channel:
            # Insert values into Channel_Table
            cursor.execute("INSERT INTO Channel_Table (Channel_Id, Channel_Name, Playlist_Id, Created_Date, Subscribers, Total_Views, Total_Videos) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (row['Channel_id'], row['Channel_Name'], row['Playlist_id'], row['Created_Date'], row['Subcribers'], row['TotalViews'], row['TotalVideos']))

            # Retrieve the generated Channel_Id
            channel_id = cursor.lastrowid

            # Insert values into Videos_Table
            for vindex, vrow in video_df[video_df['Channel_id'] == row['Channel_id']].iterrows():
                cursor.execute("INSERT INTO Videos_Table (Channel_Id, Video_Id, Video_Title, Uploaded_Date, Total_Views, Total_Likes, Total_Comments) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (channel_id, vrow['Video_id'], vrow['Video_Title'], vrow['Uploaded_Date'], vrow['Total_Views'], vrow['Total_Likes'], vrow['Total_Comments']))

                # Retrieve the generated Video_Id
                video_id = cursor.lastrowid

                # Insert values into Comments_Table
                for cindex, crow in comment_df[(comment_df['Channel_id'] == row['Channel_id']) & (comment_df['Video_id'] == vrow['Video_id'])].iterrows():
                    cursor.execute("INSERT INTO Comments_Table (Channel_Id, Video_Id, Video_Title, Comments, Replies) VALUES (?, ?, ?, ?, ?)",
                                   (channel_id, video_id, crow['Video_title'], crow['Comments'], crow['Replies']))

    # Commit the changes
    conn.commit()
    conn.close()




# Mysql query

def mysql_query(chn_name):
    url = "https://raw.githubusercontent.com/pnraj/Projects/master/YouTube_Data_Harvesting_and_Warehousing/mysqldb/YouTubeApi.db"
    db_file = wget.download(url)
    conn = sqlite3.connect(db_file)
    ch_str = "', '".join(chn_name)
    
    cu_q = f"SELECT * FROM Channel_Table WHERE CHANNEL_NAME IN ('{ch_str}')"
    ch_df = pd.read_sql(cu_q, conn) ##
    # needed to isolate ch_id from chl that are selected
    ch_id_qu = ch_df['Channel_Id'].to_list()
    # needed to select based upon the ch_id_qu
    ch_id_qu = "', '".join(ch_id_qu)
    vi_qu = f"SELECT a.Video_Id,a.Video_Title,a.Uploaded_Date,a.Total_Views,a.Total_Likes,a.Total_Comments FROM Videos_Table a JOIN Channel_Table b ON a.Channel_Id = b.Ch_id WHERE b.Channel_Id IN ('{ch_id_qu}')"
    co_qu = f"SELECT a.Video_Id,a.Video_Title,a.Comments,a.Replies FROM Comments_Table a JOIN Channel_Table b ON a.Channel_Id = b.Ch_id WHERE b.Channel_Id IN ('{ch_id_qu}')"
    
    
    vi_df = pd.read_sql(vi_qu,conn)
    com_df = pd.read_sql(co_qu,conn)
    conn.close()
    return ch_df,vi_df,com_df

def mysql_single_query(chn_name):
    url = "https://raw.githubusercontent.com/pnraj/Projects/master/YouTube_Data_Harvesting_and_Warehousing/mysqldb/YouTubeApi.db"
    db_file = wget.download(url)
    conn = sqlite3.connect(db_file)
    #ch_str = "', '".join(chn_name)
    
    cu_q = f"SELECT * FROM Channel_Table WHERE CHANNEL_NAME IN ('{chn_name}')"
    ch_df = pd.read_sql(cu_q, conn) ##
    # needed to isolate ch_id from chl that are selected
    if not ch_df.empty:
        ch_id_qu = ch_df['Channel_Id'].to_list()[0]
    # needed to select based upon the ch_id_qu
    
    vi_qu = f"SELECT a.Video_Id,a.Video_Title,a.Uploaded_Date,a.Total_Views,a.Total_Likes,a.Total_Comments FROM Videos_Table a JOIN Channel_Table b ON a.Channel_Id = b.Ch_id WHERE b.Channel_Id = '{ch_id_qu}'"
    co_qu = f"SELECT a.Video_Id,a.Video_Title,a.Comments,a.Replies FROM Comments_Table a JOIN Channel_Table b ON a.Channel_Id = b.Ch_id WHERE b.Channel_Id = '{ch_id_qu}'"
    
    
    vi_df = pd.read_sql(vi_qu,conn)
    com_df = pd.read_sql(co_qu,conn)
    conn.close()
    
    return ch_df,vi_df,com_df
