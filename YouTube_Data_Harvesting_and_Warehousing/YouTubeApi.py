import streamlit as st
import pandas as pd
from Yapi.Single_Channel import single_channel_df # here data is entered from api
from Yapi.Multi_Channel import multiple_channel_df
from Ui_files.Single_ui import sin_ui_channel,tab_ui,tab_ui1
from Ui_files.Multi_ui import multi_ui_channel,display_app_instructions,sql_textbox
from mysqldb.sqlite3a import mysql_insert,mysql_query,mysql_single_query

st.set_page_config(layout='wide')

#st.markdown("""<div style='text-align: center;'>
#<h1>Youtube Data Harvesting And Warehousing</h1></div>""", unsafe_allow_html=True)

def mdb_insert(keyword,channel_Data,video_Data,comments_data):
    from pymongo import MongoClient
    client = MongoClient(st.secrets["mongoapi"])
    db = client['youtube']
    collection_names = db.list_collection_names()

    # Find the first available name by appending a number
    new_collection_name = keyword
    counter = 1
    while new_collection_name in collection_names:
        new_collection_name = f"{keyword}{counter}"
        counter += 1 
    # Create the collection with the new name
    collection = db[new_collection_name]
    Channel_Data = {"_id":f"{new_collection_name}-Channel","Channels_Data":channel_Data}
    Videos_Data = {"_id":f"{new_collection_name}-Videos","Videos_Data":video_Data}
    Comments_Data = {"_id":f"{new_collection_name}-Comments","Comments_Data":comments_data}
    ## insert at document level
    coll_Data = [Channel_Data,Videos_Data,Comments_Data]

    for col in coll_Data:
        collection.insert_one(col)
    return new_collection_name




def mdb_queries_data(coll_name):
    
    from pymongo import MongoClient
    client = MongoClient(st.secrets["mongoapi"])
    db = client['youtube']
    collection = db[f'{coll_name}']
    ch_doc = collection.find_one({"_id":f"{coll_name}-Channel"})
    vi_doc = collection.find_one({"_id":f"{coll_name}-Videos"})
    com_doc = collection.find_one({"_id":f"{coll_name}-Comments"})
    
    return ch_doc,vi_doc,com_doc

data = {}

def get_data(col_name):
    global data

    mupr = st.button("Upload to MongoDB")

    if mupr:
        new_collection_name = mdb_insert(col_name,channel_data,vid_data,comm_data)
        ch_doc,vi_doc,com_doc = mdb_queries_data(new_collection_name)
        data = {
            "channel_data": ch_doc,
            "vid_data": vi_doc,
            "comm_data": com_doc
        }



fcol1, fcol2, fcol3 = st.columns([7, 2 , 3.4])

#keyword_placeholder = fcol4.empty()
#keyword = keyword_placeholder.text_input("Enter Your Keyword")


with fcol1:
    st.write("## :orange[Youtube Data Harvesting And Warehousing]")
    
with fcol2:
    typelist = ['Single', 'Multiple']
    def_type = typelist.index("Single")
    type = st.selectbox(" :orange[Choose Your Search Mode]", typelist, index=def_type)

with fcol3:
    if type == "Single":
        keyword = st.text_input(" :orange[Paste The Channel link]")
    elif type == 'Multiple':
        keyword = st.text_input(" :orange[Type Any Topic or Channel Name]")


if not keyword:
    #st.write("Please Choose Any one Options From Drop DownDown Menu")
    display_app_instructions()

else:

    if type == "Single":

        channel_df,video_df,comment_df1,channel_data,vid_data,comm_data = single_channel_df(keyword)
        
        Channel_Name = sin_ui_channel(channel_df,video_df,comment_df1,channel_data,vid_data,comm_data)
        col_name = Channel_Name[0]
        chl_data = None
        vi_data = None
        com_data = None

        
        
        bcol,bcol1,bcol2 = st.columns([2,0.1,7])
        with bcol:
            st.markdown('<br>', unsafe_allow_html=True) 
            st.markdown('<br>', unsafe_allow_html=True)
            get_data(col_name) # this were button to upload to mongodb 
            
                

        with bcol2:
            chl_data =data.get("channel_data")
            vi_data = data.get("vid_data")
            com_data = data.get("comm_data")
            tab_ui(chl_data,vi_data,com_data)
            # dataframe
            
        st.markdown('<hr>', unsafe_allow_html=True)    


        db_qur = False
        # here comes the query button on left and each tab have a data from mysql  on right    
        dcol,mcol1,mcol = st.columns([2,0.1,7])
        with dcol:
            st.markdown('<br>', unsafe_allow_html=True) 
            st.markdown('<br>', unsafe_allow_html=True)
            myup = st.button("Upload  to  mysql ")
            if myup:
                # channel_df,video_df,comment_df1
                mysql_insert(channel_df,video_df,comment_df1)
            
            st.markdown('<br>', unsafe_allow_html=True) 
            #st.markdown('<br>', unsafe_allow_html=True)
            myqur = st.button("Query from  mysql")
            if myqur:
                # channel_df,video_df,comment_df1
                ch_df,vi_df,com_df = mysql_single_query(col_name) 
                db_qur = True

        
        with mcol:
           qtab,qtab1 = st.tabs(['Pre_Defined Query','Custom Query'])

           with qtab:
            if db_qur == True:
                tab_ui1(ch_df,vi_df,com_df)
            with qtab1:
                csol1,csol2,csol = st.columns([3,0.1,7])
                with csol1:
                    cus_qur_df = sql_textbox()
                with csol:
                    with st.expander("Custom Query Table"):
                        if cus_qur_df is not None and not cus_qur_df.empty:
                            st.dataframe(cus_qur_df.style.hide_index().set_properties(**{'max-height': '500px', 'overflow-y': 'scroll'}), width=1200, height=200)
                        else:
                            st.write("Please Type Your Query in Text Box at left side")



    elif type == "Multiple":

        channel_df,video_df,comment_df1,channel_data,vid_data,comm_data = multiple_channel_df(keyword)

        multi_ui_channel(channel_df,video_df,comment_df1,channel_data,vid_data,comm_data)
        col_name = keyword
        chl_data = None
        vi_data = None
        com_data = None

        
       
        bcol,bcol1,bcol2 = st.columns([2,0.1,7])
        with bcol:
            st.markdown('<br>', unsafe_allow_html=True) 
            st.markdown('<br>', unsafe_allow_html=True)
            get_data(col_name) # this were button to upload to mongodb 
            # upload to mysql button comes here 
                

        with bcol2:
            chl_data =data.get("channel_data")
            vi_data = data.get("vid_data")
            com_data = data.get("comm_data")
            tab_ui(chl_data,vi_data,com_data)
            # dataframe
            
        st.markdown('<hr>', unsafe_allow_html=True)    



        # here comes the query button on left and each tab have a data from mysql  on right    
        mcol1,mcol2,mcol = st.columns([6,0.5,1])
        
        with mcol1:
           #tab_ui1(channel_df,video_df,comment_df1)
            selected_channels = st.multiselect("Select the channels for Uploading ", channel_df["Channel_Name"])
            st.write(f"### Total Selected Channel : {len(selected_channels)}")
            sel_df = channel_df.copy()
            sel_df = sel_df.drop(['Channel_link','Thumbnail'],axis=1)
            ch_db = sel_df.loc[sel_df['Channel_Name'].isin(selected_channels)] # selected channels
            ch_db_id = ch_db['Channel_id'].to_list() # channel id is isolated
            
            # sorting video_df and comment_df here
            vi_db = video_df.loc[video_df['Channel_id'].isin(ch_db_id)] # selected channels videos
            com_db = comment_df1.loc[comment_df1['Channel_id'].isin(ch_db_id)] # selected channel comments
        with mcol:
            
            st.write("") 
            st.markdown('<br>', unsafe_allow_html=True)
            myup = st.button("Upload  to  mysql ")
            if myup:
                #  sorted channels inserted here!!
                mysql_insert(ch_db, vi_db, com_db)
            # tab ui will change here 

        st.markdown('<hr>', unsafe_allow_html=True)

        qtab,qtab1 = st.tabs(['Pre_Defined Query','Custom Query'])


        with qtab:

            db_qur = False
            msol1,msol2,msol = st.columns([2,0.1,7])
            with msol1:
                st.markdown('<br>', unsafe_allow_html=True) 
                st.markdown('<br>', unsafe_allow_html=True)
                myqur = st.button("Query from  mysql")
                if myqur:
                    # channel_df,video_df,comment_df1
                    qu_ch_df,qu_vi_df,qu_com_df = mysql_query(selected_channels)
                    db_qur = True
            
            with msol: # here were the text for query will comes
                if db_qur == True:
                    tab_ui1(qu_ch_df,qu_vi_df,qu_com_df) # imported from Single_ui.py
                else:
                    st.write(" #### Press the Button On Your Left side To Query The Data From Mysql DataBase After Uploading The Data!!!")
        
        with qtab1:

            csol1,csol2,csol = st.columns([3,0.1,7])
            with csol1:
                cus_qur_df = sql_textbox()
            with csol:
                with st.expander("Custom Query Table"):
                    if cus_qur_df is not None and not cus_qur_df.empty:
                        st.dataframe(cus_qur_df.style.hide_index().set_properties(**{'max-height': '500px', 'overflow-y': 'scroll'}), width=1200, height=200)
                    else:
                        st.write("Please Type Your Query in Text Box at left side")
            
    

        st.markdown('<hr>', unsafe_allow_html=True)
 










#----------------------------- Queryied data get displayed here--------------------------------------------------
