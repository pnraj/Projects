from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pymongo import MongoClient
import pandas as pd

def Channel_data(ch_list):
    API_KEY = st.secrets["apikey1"]
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    all_id = ','.join(ch_list)
    cha_res = youtube.channels().list(
                    part='contentDetails,snippet,statistics',
                    id=all_id).execute()
    ch_ti1 = []
    for i in cha_res['items']:
            ch_id = i['id']
            channel_link = f"https://www.youtube.com/channel/{ch_id}"
            ch_title = i['snippet']['title']
            ch_playlist = i['contentDetails']['relatedPlaylists']['uploads']
            CreatedAt = i['snippet']['publishedAt']
            Subcount = i['statistics']['subscriberCount']
            TotalViews = i['statistics']['viewCount']
            TotalVideos = i['statistics']['videoCount']
            ch_logo = i['snippet']['thumbnails']['medium']['url']
            ch_ti1.append({"Channel_id": ch_id,"Channel_Name": ch_title,"Playlist_id": ch_playlist,"Created_Date":CreatedAt,
                                                    "Subcribers":Subcount,"TotalViews":TotalViews,"TotalVideos":TotalVideos,
                                                    "Thumbnail":ch_logo,"Channel_link":channel_link})
        
    
    return ch_ti1

def ch_playlist(ch_id):
    playlist_id = []
    for cid in ch_id:
        pid = cid[:1] + "U" + cid[2:]
        playlist_id.append(pid)
    return playlist_id

def get_video_ids(playid):
    API_KEY = st.secrets["apikey2"]
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    video_ids = []
    for pid in playid:
        try:
            request = youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId=pid,
                        maxResults=50)  ## giving options to users to query total no of videos get details
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])


        except HttpError as e:
            error = e.resp.get("error")
            if error is not None and 'errors' in error and error['errors'][0]['reason'] == "playlistNotFound":
                # Skip processing this playlist ID and move to the next iteration
                continue
            else:
                # Handle other types of errors
                print("An error occurred:", error)

    return video_ids

## new version of get_video_details
def get_video_details(video_ids):
    API_KEY = st.secrets["apikey3"]
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    all_video_stats = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for video in response['items']:
            ch_id = video['snippet']['channelId']
            Video_Id = video['id']
            Title = video['snippet']['title']
            Published_date = video['snippet']['publishedAt']
            
            try:
                Views = video['statistics']['viewCount']
                Likes = video['statistics']['likeCount']
                Comments = video['statistics']['commentCount']
                
                all_video_stats.append({"Channel_id": ch_id,"Video_id":Video_Id,"Video_Title":Title,"Uploaded_Date":Published_date,
                                                           "Total_Views":Views,"Total_Likes":Likes,
                                                                  "Total_Comments":Comments})
            except KeyError:
                # Skip the item if any of the required keys are missing
                continue
    
    return all_video_stats

## Search function
def first_search(keyword):
    API_KEY = st.secrets["apikey1"]
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    search_response = youtube.search().list(
                    q=keyword,
                    part="snippet",
                    maxResults=10,
                    type="channel",
                    order="relevance",
                    regionCode="IN" ).execute()
    
    ch_ti = []
    for i in search_response['items']:
        ch_id = i['snippet']['channelId']
        if not ch_id in ch_ti:
            ch_ti.append(ch_id)
    return ch_ti


def comment_data(vid_lis):
    API_KEY = st.secrets["apikey4"]
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    comments = []
    for vids in vid_lis:
        try:
            ch_response = youtube.videos().list(
                part='snippet',
                id=vids).execute()

            for video in ch_response['items']:
                ch_id = video['snippet']['channelId']
                vid_title = video['snippet']["title"]
                Channel_title = video['snippet']["channelTitle"]

            response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=vids,
                maxResults=30,
            ).execute()
            
            video_comments = []
            for item in response['items']:
                
                comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
                #reply_count = item['snippet']["totalReplyCount"]
                
                
                repl = []
                if 'replies' in item:
                    replies = item['replies']['comments']
                    for reply in replies:
                        reply_text = reply['snippet']['textOriginal']
                        repl.append(reply_text)

                else:
                    repl = ["No reply"]
                
                video_comments.append({"Comments":comment,"Replies": repl})
            comments.append({"Channel_id":ch_id,"Video_id": vids,"Video_title":vid_title,"Comments":video_comments})

        except HttpError as e:
            if e.resp.status == 403:
                pass

    return comments

def multiple_data(keyword):
    channel_id = first_search(keyword)
    playlist_id = ch_playlist(channel_id)
    channel_Data = Channel_data(channel_id) ##
    vid_ids = get_video_ids(playlist_id)
    video_Data = get_video_details(vid_ids) ##
    comments_data = comment_data(vid_ids) ##
    
    return channel_Data,video_Data,comments_data


def process_comment(comment_df):
    cdf_df = comment_df['Comments'].to_frame()
    cdf_df1 = cdf_df.applymap(lambda x: [] if x == [] else x)  # convert empty list into []
    rldf = pd.DataFrame({})

    for i, row in cdf_df1.iterrows():
        comments = row['Comments']
        if comments:
            for comment_dict in comments:
                temp_df = comment_df.loc[[i]].copy()
                if 'Replies' in comment_dict and comment_dict['Replies']:
                    temp_df.at[i, 'Replies'] = ', '.join(comment_dict['Replies'])
                else:
                    temp_df.at[i, 'Replies'] = "No Replies"
                temp_df.at[i, 'Comments'] = comment_dict['Comments']
                rldf = pd.concat([rldf, temp_df], ignore_index=True)
        else:
            temp_df = comment_df.loc[[i]].copy()
            temp_df.at[i, 'Replies'] = "No Replies"
            temp_df.at[i, 'Comments'] = "No Comments"
            rldf = pd.concat([rldf, temp_df], ignore_index=True)

    # combining final data
    #com_df1 = rldf.drop('Comments', axis=1)
    
    return rldf
import streamlit as st
import numpy as np
@st.cache_data
def multiple_channel_df(channel_link):
    channel_data,vid_data,comm_data = multiple_data(channel_link)
    channel_df = pd.DataFrame(channel_data)
    channel_df[['Subcribers','TotalViews','TotalVideos']] = channel_df[['Subcribers','TotalViews','TotalVideos']].astype(np.int64)
    channel_df['Created_Date'] = pd.to_datetime(channel_df['Created_Date']).dt.strftime('%d-%m-%Y')

    video_df = pd.DataFrame(vid_data)
    video_df[['Total_Views','Total_Likes', 'Total_Comments']] = video_df[['Total_Views','Total_Likes', 'Total_Comments']].astype(np.int64)
    video_df['Uploaded_Date'] = pd.to_datetime(video_df['Uploaded_Date']).dt.strftime('%d-%m-%Y')

    comment_df = pd.DataFrame(comm_data)
    comment_df1 = process_comment(comment_df)
    
    return channel_df,video_df,comment_df1,channel_data,vid_data,comm_data
