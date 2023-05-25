import streamlit as st
import pandas as pd
import sqlite3


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

def display_app_instructions():
    # Center-align the heading
    st.markdown("<h3 style='text-align: center;'>&#x1F680 How To Use &#x1F680; </h3>", unsafe_allow_html=True)
    col1, col2,col3 = st.columns([6,3,3.5])

    # GitHub link
    github_link = "#### :orange[GitHub Link]: [Click Here](https://github.com/pnraj)"
    col1.markdown(github_link)

    # LinkedIn link
    linkedin_link = "#### :orange[LinkedIn Link]: [Click Here](https://www.linkedin.com/in/nataraj-palanivel-057085144/)"
    col3.markdown(linkedin_link)

    # Describe the app's modes and instructions
    #st.markdown("There are two modes available in this app:")
    st.markdown("<h5 style='text-align: center;'>&#x2714 There are two modes available in this app: &#x2714; </h5>", unsafe_allow_html=True)
    # Single Mode description
    single_mode_title = "###### :one: Single Mode "
    single_mode_description = (" - Please copy the **URL** of your desired **YouTube channel** and paste it in the text box." 
    "For example: `https://www.youtube.com/@andreaskayy`" 
    " - This mode will fetch the latest **100 videos** and details of their **comments and replyies**(up to 30 comments per video)."  
    " - It usually takes less than **one minute**.")

    # Display the Single Mode description
    st.markdown(single_mode_title)
    st.markdown(single_mode_description)

    # Multiple Mode description
    multiple_mode_title = "###### :two: Multiple Mode "
    multiple_mode_description = (" - Please type the **niche or topics** related to the **YouTube channels** you're interested in the text box."
    " - This mode will fetch the latest **50 videos** / **Channel** and details of their **comments and replyies** (up to 30 comments per video). It usually takes less than **three minutes**.")

    # Display the Multiple Mode description
    st.markdown(multiple_mode_title)
    st.markdown(multiple_mode_description)

    st.markdown("<h4 style='text-align: left; color: purple;'>My Other Projects links</h4>", unsafe_allow_html=True)

    # Display the link
    st.markdown("[GeoVisualization of PhonePhe Pulse](https://pnraj-projects-phonephe-pulsedashboard-y5wmx8.streamlit.app/)")


def multi_ui_channel(channel_df,video_df,comment_df1,channel_data,vid_data,comm_data):
    ## channel_df processed here
    Channel_Name = channel_df['Channel_Name'].to_list()

    scol1,scol2,scol3 = st.columns([4.2,0.1,7])

    with scol1:
        # Channel,pubDate,tSub,tVid,tLik,tViw = None # these values must be query from mongodb
        chan_names = Channel_Name
        chan_name = st.selectbox(" :orange[Choose Channel Name]", chan_names)
        selected_Chan_Name = channel_df.loc[channel_df['Channel_Name'] == chan_name]
        #        
        Channel_Date = selected_Chan_Name['Created_Date'].to_list()[0]
        Channel_sub = format_number(selected_Chan_Name['Subcribers'].to_list()[0])
        Channel_views = format_number(selected_Chan_Name['TotalViews'].to_list()[0])
        Channel_VidCont = format_number(selected_Chan_Name['TotalVideos'].to_list()[0])
        Channel_link = selected_Chan_Name['Channel_link'].to_list()[0]
        Channel_thumb = selected_Chan_Name['Thumbnail'].to_list()[0]
        selected_cid = selected_Chan_Name['Channel_id'].to_list()[0]  # needed for videos sorting

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
        
        
        
        #st.markdown('<hr>', unsafe_allow_html=True)
        
    #------------------------------------Video data ---------------------------------------------
    #selected_cid=channel_df.loc[channel_df['Channel_Name']==Channel_Name,'Channel_id'].to_list()[0]
    selected_chn_vid = video_df[video_df['Channel_id'] == selected_cid]
    all_vid_list = selected_chn_vid['Video_Title'].to_list() 

    with scol3:
        vid_names = all_vid_list
        vid_name = st.selectbox(" :orange[Choose Your Video Name]",vid_names)
        
        selected_vid = video_df.loc[video_df['Video_Title'] == vid_name, 'Video_id'].to_list()[0] ## needed for comments sorting
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

        
    
        selected_com = comment_df1.loc[comment_df1['Video_id'] == selected_vid, ['Comments','Replies']].reset_index(drop=True)
        st.dataframe(selected_com.style.hide_index().set_properties(**{'max-height': '500px', 'overflow-y': 'scroll'}), width=1200, height=198)

        #st.info("Mongodb Db name, collection name displayed here")
        
        
    st.markdown('<hr>', unsafe_allow_html=True)



def sql_textbox():

    conn = sqlite3.connect('YouTubeApi.db')
    cursor = conn.cursor()
    # Text input widget for SQL query
    query = st.text_area('Enter SQL query', key='query-input', height=300)

    # Execute SQL query and display results
    if st.button('Execute', key='execute-btn'):
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            if len(results) > 0:
                # Convert results to DataFrame
                df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
                return df
            else:
                st.write('No results found.')
        except Exception as e:
            st.error(f'Error executing SQL query: {str(e)}')

    # Close the database connection
    conn.close()

    