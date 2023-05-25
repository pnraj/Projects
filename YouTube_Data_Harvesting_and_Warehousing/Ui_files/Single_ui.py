import streamlit as st
import time



def format_number(n):
    if n < 1000:
        return str(n)
    elif n < 1000000:
        formatted = f"{n / 1000:.2f}"
        if formatted.endswith('.00'):
            formatted = formatted[:-3]
        elif formatted.endswith('0'):
            formatted = formatted[:-1]
        return formatted + "k"
    else:
        formatted = f"{n / 1000000:.2f}"
        if formatted.endswith('.00'):
            formatted = formatted[:-3]
        elif formatted.endswith('0'):
            formatted = formatted[:-1]
        return formatted + "M"
    





def sin_ui_channel(channel_df,video_df,comment_df1,channel_data,vid_data,comm_data):
    ## channel_df processed here

    
    Channel_Name = channel_df['Channel_Name'].to_list()
    Channel_Date = channel_df['Created_Date'].to_list()[0]
    Channel_sub = format_number(channel_df['Subcribers'].to_list()[0])
    Channel_views = format_number(channel_df['TotalViews'].to_list()[0])
    Channel_VidCont = format_number(channel_df['TotalVideos'].to_list()[0])
    Channel_link = channel_df['Channel_link'].to_list()[0]
    Channel_thumb = channel_df['Thumbnail'].to_list()[0]

    ##
    
    scol1,scol2,scol3 = st.columns([4.2,0.1,7])

    with scol1:
        # Channel,pubDate,tSub,tVid,tLik,tViw = None # these values must be query from mongodb
        chan_names = Channel_Name
        chan_name = st.selectbox(" :orange[Choose Channel Name]", chan_names)
        #          
        tcol1, tcol2, tcol3 = st.columns([4, 0.1, 8])

        with tcol1:
            st.image(Channel_thumb, width=150)

        with tcol3:
            #st.markdown('<br>', unsafe_allow_html=True)
            st.write("<h4 style='text-align: center; color: orange;'>Channel Created Date</h4>", unsafe_allow_html=True)
            st.markdown(f"""<div style='text-align: center;'>
                                <h4>{Channel_Date}</h4>
                            </div>""", unsafe_allow_html=True)
            link_html = f"<div style='text-align: center;'><a href={Channel_link} target='_blank'>Channel Link</a></div>"
            st.markdown(link_html, unsafe_allow_html=True)
            
        st.markdown('<br>', unsafe_allow_html=True)    
        titl1, titl2,titl3 = st.columns([2.5, 3,3])

        with titl1:
            st.markdown("<h4 style='text-align: center; color: orange;'>Total Views</h4>", unsafe_allow_html=True)
            st.markdown(f"""<div style='text-align: center;'>
                                <h5>{Channel_views}</h5>
                            </div>""", unsafe_allow_html=True)

        with titl2:
            st.markdown("<h4 style='text-align: center; color: orange;'>Total Videos</h4>", unsafe_allow_html=True)
            st.markdown(f"""<div style='text-align: center;'>
                                <h5>{Channel_VidCont}</h5>
                            </div>""", unsafe_allow_html=True)
        
        with titl3:
            st.markdown("<h4 style='text-align: center; color: orange;'>Subcribers</h4>", unsafe_allow_html=True)
            st.markdown(f"""<div style='text-align: center;'>
                                <h5>{Channel_sub}</h5>
                            </div>""", unsafe_allow_html=True)
       

            #st.write(new_collection_name)
       
        #st.markdown('<hr>', unsafe_allow_html=True)
        
    #------------------------------------Video data ---------------------------------------------
    all_vid_list = video_df['Video_Title'].to_list() # single channel so no need for id reference but multichannel needed

    with scol3:
        vid_names = all_vid_list
        vid_name = st.selectbox(" :orange[Choose Your Video Name]",vid_names)
        #selected_cid=channel_df.loc[channel_df['Channel_Name']==Channel_Name,'Channel_id'].to_list()[0]
        #selected_chn_vid = video_df[video_df['Channel_id'] == selected_cid]
        selected_vid = video_df.loc[video_df['Video_Title'] == vid_name, 'Video_id'].to_list()[0]
        selected_vid_data = video_df.loc[video_df['Video_id'] == selected_vid ,['Uploaded_Date','Total_Views','Total_Likes','Total_Comments']]
        vid_upload = selected_vid_data['Uploaded_Date'].to_list()[0]
        vid_views = format_number(selected_vid_data['Total_Views'].to_list()[0])
        vid_likes = format_number(selected_vid_data['Total_Likes'].to_list()[0])
        vid_com = format_number(selected_vid_data['Total_Comments'].to_list()[0])

        stitl1, stitl2,stitl3,stitl4 = st.columns([3, 3,3,2])

        with stitl1:
            st.markdown("<h4 style='text-align: center; color: orange;'>Uploaded Date</h4>", unsafe_allow_html=True)
            st.markdown(f"""<div style='text-align: center;'>
                                <h5>{vid_upload}</h5>
                            </div>""", unsafe_allow_html=True)

        with stitl2:
            st.markdown("<h4 style='text-align: center; color: orange;'>No Of Comments</h4>", unsafe_allow_html=True)
            st.markdown(f"""<div style='text-align: center;'>
                                <h5>{vid_com}</h5>
                            </div>""", unsafe_allow_html=True)

        with stitl3:
            st.markdown("<h4 style='text-align: center; color: orange;'>No Of Views</h4>", unsafe_allow_html=True)
            st.markdown(f"""<div style='text-align: center;'>
                                <h5>{vid_views}</h5>
                            </div>""", unsafe_allow_html=True)
        
        with stitl4:
            st.markdown("<h4 style='text-align: center; color: orange;'>Likes</h4>", unsafe_allow_html=True)
            st.markdown(f"""<div style='text-align: center;'>
                                <h5>{vid_likes}</h5>
                            </div>""", unsafe_allow_html=True)
    #---------------------------------------- video comments -------------------------------------------------

        
    
        selected_com = comment_df1.loc[comment_df1['Video_id'] == selected_vid, ['Comments','Replies']].reset_index(drop=True) ## df
        selected_com = selected_com.set_index('Comments')
    
        st.dataframe(selected_com.style.set_properties(**{'max-height': '500px', 'overflow-y': 'scroll'}), width=1200, height=198)
        #st.info("Mongodb Db name, collection name displayed here")
        
        
    st.markdown('<hr>', unsafe_allow_html=True)
    #st.write(chl_data)
    
    return Channel_Name

@st.cache_data
def tab_ui(chl_data,vi_data,com_data):
    tab1,tab2,tab3 = st.tabs(['Channel Data','Videos Data','Comments Data'])
    with tab1:
        with st.expander("Channel Data"):
            chl_slot = st.empty()
            if chl_data:
                chl_slot.json(chl_data,expanded=False)
    with tab2:
        with st.expander("Videos Data"):
            vid_slt = st.empty()
            if chl_data:
                vid_slt.json(vi_data,expanded=False)
    with tab3:
        with st.expander("Comments Data"):
            com_slt = st.empty()
            if chl_data:
                com_slt.json(com_data,expanded=False)

def tab_ui1(channel_df,video_df,comment_df1):
    tab1,tab2,tab3 = st.tabs(['Channel table','Videos Table','Comments Table'])
    with tab1:
        with st.expander("Channel Tables"):
            chl_slot = st.empty()
            if channel_df:
                channel_df.set_index('Channel_Name')
                chl_slot.dataframe(channel_df)
    with tab2:
        with st.expander(" Video Tables"):
            vid_slt = st.empty()
            if video_df:
                vid_slt.dataframe(video_df)
        
    with tab3:
        with st.expander("Comments Tables"):
            com_slt = st.empty()
            if comment_df1:
                com_slt.dataframe(comment_df1)

        
