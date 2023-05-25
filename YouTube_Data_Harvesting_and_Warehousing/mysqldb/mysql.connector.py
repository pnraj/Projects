import mysql.connector

def mysql_insert(channel_df, video_df, comment_df):
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host='your_host',
        user='your_user',
        password='your_password',
        database='your_database'
    )
    cursor = conn.cursor()

    ch_schema = """
        CREATE TABLE IF NOT EXISTS Channel_Table (
            ch_id INT AUTO_INCREMENT PRIMARY KEY,
            Channel_Id VARCHAR(30),
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
            vid_id INT AUTO_INCREMENT PRIMARY KEY,
            Channel_Id INT,
            Video_Id VARCHAR(20),
            Video_Title VARCHAR(100),
            Uploaded_Date DATETIME,
            Total_Views BIGINT,
            Total_Likes BIGINT,
            Total_Comments BIGINT,
            FOREIGN KEY (Channel_Id) REFERENCES Channel_Table (ch_id)
        )
    """

    comm_schema = """
        CREATE TABLE IF NOT EXISTS Comments_Table (
            com_id INT AUTO_INCREMENT PRIMARY KEY,
            Channel_Id INT,
            Video_Id INT,
            Video_Title VARCHAR(100),
            Comments VARCHAR(200),
            Replies VARCHAR(200),
            FOREIGN KEY (Channel_Id) REFERENCES Channel_Table (ch_id),
            FOREIGN KEY (Video_Id) REFERENCES Videos_Table (vid_id)
        )
    """

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")  # Enable foreign key support

    cursor.execute(ch_schema)
    cursor.execute(vi_schema)
    cursor.execute(comm_schema)

    for index, row in channel_df.iterrows():
        # Insert values into Channel_Table
        cursor.execute("""
            INSERT IGNORE INTO Channel_Table (Channel_Id, Channel_Name, Playlist_Id, Created_Date, Subscribers, Total_Views, Total_Videos)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Channel_id'],
            row['Channel_Name'],
            row['Playlist_id'],
            row['Created_Date'],
            row['Subcribers'],
            row['TotalViews'],
            row['TotalVideos']
        ))

        # Retrieve the generated Channel_Id
        channel_id = cursor.lastrowid

        # Insert values into Videos_Table
        for vindex, vrow in video_df[video_df['Channel_id'] == row['Channel_id']].iterrows():
            cursor.execute("""
                INSERT IGNORE INTO Videos_Table (Channel_Id, Video_Id, Video_Title, Uploaded_Date, Total_Views, Total_Likes, Total_Comments)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                channel_id,
                vrow['Video_id'],
                vrow['Video_Title'],
                vrow['Uploaded_Date'],
                vrow['Total_Views'],
                vrow['Total_Likes'],
                vrow['Total_Comments']
            ))

            # Retrieve the generated Video_Id
            video_id = cursor.lastrowid

            # Insert values into Comments_Table
            for cindex, crow in comment_df[
                (comment_df['Channel_id'] == row['Channel_id']) &
                (comment_df['Video_id'] == vrow['Video_id'])
            ].iterrows():
                cursor.execute("""
                    INSERT IGNORE INTO Comments_Table (Channel_Id, Video_Id, Video_Title, Comments, Replies)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    channel_id,
                    video_id,
                    crow['Video_title'],
                    crow['Comments'],
                    crow['Replies']
                ))

    # Commit the changes
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()
