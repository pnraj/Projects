import re
import requests
import pandas as pd
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


#channel_id_extract(channel_link)
def Channel_data(all_id):
    API_KEY = "AIzaSyDldORJbO8akDKDJ9XGFvmzoqTCiCbpgTo"
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
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
# video id 
def get_video_ids(playlist_id):
    API_KEY = "AIzaSyDldORJbO8akDKDJ9XGFvmzoqTCiCbpgTo"
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    video_ids = []

    try:
        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50
        )

        counter = 0  # Counter for tracking the number of video IDs

        while request and counter < 100:  # Stop when 100 video IDs are obtained
            response = request.execute()
            for item in response['items']:
                video_ids.append(item['contentDetails']['videoId'])
                counter += 1

            request = youtube.playlistItems().list_next(request, response)

    except HttpError as e:
        error_message = e.content.decode("utf-8")
        print("An error occurred:", error_message)

    return video_ids[:100] 

## new version of get_video_details
def get_video_details(video_ids):
    API_KEY = "AIzaSyDldORJbO8akDKDJ9XGFvmzoqTCiCbpgTo"
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    #video_ids = video_ids[:100]
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

def comment_data(vid_lis):
    API_KEY = "AIzaSyDldORJbO8akDKDJ9XGFvmzoqTCiCbpgTo"
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
# custome made function
def ch_playlist(cid):
    pid = cid[:1] + "U" + cid[2:]
    return pid


def chn_id_get(channel_link):
    if "@" in channel_link:
        channel_url = channel_link+"/about"

        response = requests.get(channel_url) # Send a GET request to the channel page

        channel_id_match = re.search(r'"channelId":"([A-Za-z0-9_-]+)"', response.text) # Extract the channel ID using regular expressions

        if channel_id_match:
            channel_id = channel_id_match.group(1)
        channel_data = Channel_data(channel_id)    
       
    elif "/UC" in channel_link:
        channel_id = channel_link.split('/')[-1]
        channel_data = Channel_data(channel_id)
    else:
        st.write(" #### Please Enter Correct Url Of the YouTube Channel")
    
    return channel_data,channel_id

def single_channel_data(channel_link):
    channel_data,channel_id = chn_id_get(channel_link)
    playid = ch_playlist(channel_id)
    vid_id = get_video_ids(playid)
    vid_data = get_video_details(vid_id)
    comm_data = comment_data(vid_id)
    
    return channel_data,vid_data,comm_data
# comment data processed here 
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


    
    return rldf

import numpy as np
@st.cache_data
def single_channel_df(channel_link):
    channel_data,vid_data,comm_data = single_channel_data(channel_link)
    #channel df
    channel_df = pd.DataFrame(channel_data)
    channel_df[['Subcribers','TotalViews','TotalVideos']] = channel_df[['Subcribers','TotalViews','TotalVideos']].astype(np.int64)
    channel_df['Created_Date'] = pd.to_datetime(channel_df['Created_Date']).dt.strftime('%d-%m-%Y')
    #video df
    video_df = pd.DataFrame(vid_data)
    video_df[['Total_Views','Total_Likes', 'Total_Comments']] = video_df[['Total_Views','Total_Likes', 'Total_Comments']].astype(np.int64)
    video_df['Uploaded_Date'] = pd.to_datetime(video_df['Uploaded_Date']).dt.strftime('%d-%m-%Y')
    #Comment df
    comment_df = pd.DataFrame(comm_data)
    comment_df1 = process_comment(comment_df)
    
    return channel_df,video_df,comment_df1,channel_data,vid_data,comm_data



