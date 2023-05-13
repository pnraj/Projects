import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.subplots as sp
import plotly.graph_objects as go
import json
import wget
import locale
import warnings
import requests
warnings.filterwarnings("ignore")
from db import users_df,trans_df,pin_df,pay_df
#from files.db import data_fetch,queries
## seting page config as wide
st.set_page_config(layout='wide')
### Title columns

t1,c1,c2,c4=st.columns([8,1,1,2])
with t1:
    title_html = '''
    <h1 style="text-align: center; color: green;">
        <a href="https://github.com/pnraj/Projects/tree/master/Phonephe_Pulse" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: green;">
            ₹PhonePe Pulse 2018-2022 Analysis
        </a>
    </h1>
'''
    st.markdown(title_html, unsafe_allow_html=True)
    #title_link = '[PhonePe Pulse 2018-2022 Analysis](https://github.com/pnraj/Projects/tree/master/Phonephe_Pulse)'
    #st.write(f'# :green[₹{title_link} :chart_with_upwards_trend:]')
with c1:
    y = ['2018', '2019', '2020','2021','2022']
    default_y = y.index("2022")
    year = st.selectbox('',
            y,key='year',index=default_y)
with c2:
    q = ['Q1', 'Q2', 'Q3','Q4']
    default_qua = q.index("Q1")
    qua = st.selectbox('',
            q,key='quarter',index=default_qua)
    if qua == 'Q1':
        quarter = 1
    elif qua == 'Q2':
        quarter = 2
    elif qua == 'Q3':
        quarter = 3
    elif qua == 'Q4':
        quarter = 4
with c4:
    options = ["Users", "Transactions"]
    default_index = options.index("Transactions")
    u_t = st.selectbox("", options,key='u_t',index=default_index)

### users map data get processed from here
def formated(number):
    number_str = str(number)
    length = len(number_str)
    formatted_number = ""
    for i, digit in enumerate(number_str):
        formatted_number = digit + formatted_number
        if (length - i) % 2 == 0 and i != length - 1:
            formatted_number = "," + formatted_number
    return formatted_number
url = 'https://github.com/pnraj/Projects/raw/master/Phonephe_Pulse/states_india.geojson'

response = requests.get(url)
with open('states_india.geojson', 'wb') as file:
    file.write(response.content)

india_states = gpd.read_file('states_india.geojson')
# Creating id needed for map ++++++++++++++++++++
df2 = india_states.copy()
df2 = df2.rename(columns={'st_nm': 'state', 'state_code': 'id'})
df2 = df2[['id', 'state']]
gid = df2.sort_values('state')
tr_map = gid.copy()
#++++++++++++++++++++++++++++++++++++
# files are imported from the db.py file

#users_df,trans_df,pin_df,pay_df = data_fetch(queries) 
# users data
ur_df = users_df.copy()
map_df2 = ur_df.loc[(ur_df['Quarter']==int(quarter)) & (ur_df['Year']==int(year))].sort_values(by='StateName') 
map_df2['AppOpening'] = map_df2['AppOpening'].astype(float)

#map_df2['StNames'] = tr_map['state'] ## creating a column for referencing the id with same state in geojson
map_df3 = map_df2.groupby('StateName').agg({'UsersCount':'sum','AppOpening':'sum'}).reset_index()
map_df3[['id','StNames']] = tr_map[['id','state']]
map_df3['StateName'] = map_df3['StateName'].apply(lambda x: str(x)).apply(lambda x: x.capitalize())
map_df3['Registered Users'] = map_df3['UsersCount'].apply(lambda x: formated(round(x)) if pd.notnull(x) else '')
map_df3[f'App Opens in Q{quarter}'] = map_df3['AppOpening'].apply(lambda x: formated(round(x)) if pd.notnull(x) else '')
snd = map_df3.copy()
 ## users map

fig = px.choropleth_mapbox(
        snd,
        locations="id",
        geojson=india_states,
        color="UsersCount",
        hover_name="StateName",
        hover_data={'Registered Users':True,map_df3.columns[6]:True,'id':False,'UsersCount':False},
        title=f"PhonePe Total Users in Q {quarter}-{year}",
        mapbox_style="carto-positron",
        center={"lat": 24, "lon": 79},
        color_continuous_scale=px.colors.diverging.PuOr,
        color_continuous_midpoint=0,
        zoom=3.6,
        width=800, 
        height=800
    ) 
fig.update_layout(coloraxis_colorbar=dict(title=' ', showticklabels=True),title={
        'font': {'size': 24}
    },hoverlabel_font={'size': 18})
## Transaction button data
pay_map = pay_df.copy()
map_df = pay_map.loc[(pay_map['Quarter']==int(quarter)) & (pay_map['Year']==int(year))]
map_df1 = map_df.groupby('StateName').agg({'TransactionCounts':'sum','TransactionAmounts':'sum'}).reset_index()
map_df1[['id','StNames']] = tr_map[['id','state']]
#map_df1['StNames'] = tr_map['state']
fst = map_df1.copy()
fst['id'] = fst['id'].astype(int)
def mcrores(number):
    return '₹'+'{:,.0f} Cr'.format(round(number / 10000000))

fst['StateName'] = fst['StateName'].apply(lambda x: x.capitalize())    
fst['All Transactions'] = fst['TransactionCounts'].apply(lambda x: round(x)).apply(lambda x: formated(x))
fst['Total Payment Values'] = fst['TransactionAmounts'].apply(lambda x: round(x)).apply(lambda x: mcrores(x))
fst['Avg.Transaction Value'] = fst['TransactionAmounts'] / fst['TransactionCounts']
fst['Avg.Transaction Value'] = fst['Avg.Transaction Value'].apply(lambda x: round(x)).apply(lambda x: "₹{:,.0f}".format(x))
## Transaction map
fig1 = px.choropleth_mapbox(
    fst,
    locations="id",
    geojson=india_states,
    color="TransactionAmounts",
    hover_name="StateName",
    hover_data={'All Transactions':True,'Total Payment Values':True,'id':False,'Avg.Transaction Value':True,'TransactionAmounts':False},
    title=f"PhonePe Amounts Transactions in Q {quarter}-{year}",
    mapbox_style="carto-positron",
    center={"lat": 24, "lon": 79},
    color_continuous_scale=px.colors.diverging.PuOr,
    color_continuous_midpoint=0,
    zoom=3.6,
    width=800, 
    height=800
)
fig1.update_layout(coloraxis_colorbar=dict(title=' ', showticklabels=True),title={
        'font': {'size': 24}
    },hoverlabel_font={'size': 18})
### Transaction values
tr = trans_df.copy()
filter_tr = tr.loc[(tr['Year']==int(year)) & (tr['Quarter']==int(quarter))]
gr_tr = filter_tr.groupby('Year').sum()
All_transactions = gr_tr['TotalTransactionCount'].to_list()[0]
Total_payments =gr_tr['TotalTransactionAmount'] #for formating
Total_payments1 =gr_tr['TotalTransactionAmount'].to_list()[0]# ****All Transaction****
reversed_numbers = [segment[:] for segment in str(All_transactions).split(",")]
reversed_number = ",".join(reversed_numbers)
def format_number(number):
    return "{:,}".format(x)
atl = format_number(All_transactions)
#atl = "{:,}".format(All_transactions)
Avg_Transaction = round(Total_payments1/All_transactions)# *** Averege transaction value
av_form = '₹{:,}'.format(Avg_Transaction)
# Set the locale to Indian English
sf1 = Total_payments.apply(lambda x: "₹" + "{:,.0f}".format(x/10000000) + "Cr")

trvalue1 = sf1.to_list()[0] # ***Total payments 

## Users section values

ur = users_df.copy()
ur['AppOpening'] = ur['AppOpening'].astype(float)
filter_ur = ur.loc[(ur['Year']==int(year)) & (ur['Quarter']==int(quarter))]
gr_ur = filter_ur.groupby('Year').sum()
Registered_users = gr_ur['UsersCount'].to_list()[0] #****Registered users****
reg_usr = formated(Registered_users)
App_opens = int(gr_ur['AppOpening'].to_list()[0]) #****App opens****
app_on = formated(App_opens)

## Top 10 values
a = users_df.copy()
def crores(number):
    return '{:.2f}Cr'.format(number / 10000000)
#Top 10 district
filter_ds = a.loc[(a['Year']==int(year)) & (a['Quarter']==int(quarter))]
pin_d = filter_ds.groupby(['Year','DistrictName']).sum().reset_index()
top_10_dist = pin_d.nlargest(10, 'UsersCount')[['DistrictName', 'UsersCount']]
df_d = top_10_dist.copy()
df_d['DistrictName'] = df_d['DistrictName'].apply(lambda x: x.title())
df_d['UsersCount'] = df_d['UsersCount'].apply(lambda x: crores(x)) # top 10 districts
df_d = df_d.reset_index(drop=True)
df_d.index += 1
#-----
#Top 10 states
filter_st = a.loc[(a['Year']==int(year)) & (a['Quarter']==int(quarter))]
pin_s = filter_st.groupby(['Year','StateName']).sum().reset_index()
top_10_sts = pin_s.nlargest(10, 'UsersCount')[['StateName', 'UsersCount']]
df_s = top_10_sts.copy()
df_s['StateName'] = df_s['StateName'].apply(lambda x: x.title())
df_s['UsersCount'] = df_s['UsersCount'].apply(lambda x: crores(x)) # top 10 states
df_s = df_s.reset_index(drop=True)
df_s.index += 1
#---------------------------------------------------------------#
#Top 10 Pincodes
pr = pin_df.copy()
filter_pr = pr.loc[(pr['Year']==int(year)) & (pr['Quarter']==int(quarter))]
pin = filter_pr.groupby(['Year','Pincode']).sum().reset_index()
top_10_pins = pin.nlargest(10, 'Total_Registered_users')[['Pincode', 'Total_Registered_users']]
def lakh(number):
    return '{:.2f}L'.format(number / 100000)
df_p = top_10_pins.copy()
df_p['UsersCount'] = df_p['Total_Registered_users'].apply(lambda x: lakh(x))
df_p = df_p.reset_index(drop=True)
df_p.index += 1
#-----------------
#payments method groupby
at = pay_df.copy()
atr = at.loc[(at['Year']==int(year)) & (at['Quarter']==int(quarter))]
atr1 = atr.groupby(['Year', 'TransactionMethod']).sum()
df1a = atr1.reset_index().sort_values(by='TransactionCounts', ascending=False).reset_index(drop=True).drop(['Year', 'Quarter', 'TransactionAmounts'], axis=1)

df1a = df1a.drop(3).append(df1a.loc[3]).reset_index().drop('index',axis=1)
df1a['TransactionCounts'] = df1a['TransactionCounts'].apply(lambda x: format_number(x))# this will be dataframe that inserted into
df1a = df1a.reset_index(drop=True)
df1a.index += 1

s1,s2 = st.columns([8,4])

with s1:

    # users map
    if u_t == "Users":
        st.plotly_chart(fig, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False)
        
    # transaction map
    else:
        st.plotly_chart(fig1, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False)
        
with s2:

    if u_t == "Users":
        st.subheader(u_t)
        st.subheader(f":green[Registered Users Till {qua} {year}] ")
        st.write(f'#### {reg_usr}')## values
        st.write('')
        st.subheader(f':green[ App Opens in {qua} {year}]')
        st.write(f'#### {app_on}')## values
        st.markdown('<hr>', unsafe_allow_html=True)
        tb10 = st.selectbox('', ('Top 10 States','Top 10 Districts','Top 10 Pincodes'),key='top10')
        if tb10 == 'Top 10 Districts':
            st.dataframe(df_d, width=800)
        elif tb10 == 'Top 10 States':
            st.dataframe(df_s, width=800)
        else:
            st.dataframe(df_p, width=800)

    
    else:
        st.write(f'## {u_t}')
        st.write('#### :green[All Transactions (UPI+Cards+Wallets)]')
        st.write(f'#### {atl}')## values
        st.write('')

        rc1,rc2 = st.columns([1,1])
        with rc1:
            st.write('##### :green[Total payment value]')
            st.write(f'#### {trvalue1}')## values
        with rc2:
            st.write('##### :green[Avg.transaction value]')
            st.write(f'#### {av_form}')## values
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader('Categories')
        #st.dataframe(df1a, width=800,use_container_width=True)
        #st.table(df1a.style.set_table_attributes("style='height:1000000%;'"))
        fc1,fc2 = st.columns([1.3,0.45])
        with fc1:
            mrch = df1a['TransactionMethod'][1]
            st.write(f'#### :green[{mrch}]')
            st.write('')
            peer = df1a['TransactionMethod'][2]
            st.write(f'#### :green[{peer}]')
            st.write('')
            rech = df1a['TransactionMethod'][3]
            st.write(f'#### :green[{rech}]')
            st.write('')
            fin = df1a['TransactionMethod'][4]
            st.write(f'#### :green[{fin}]')
            st.write('')
            oth = df1a['TransactionMethod'][5]
            st.write(f'#### :green[{oth}]')
        with fc2:
            val1 = df1a['TransactionCounts'][1]
            st.write(f'#### {val1}')
            st.write('')
            val2 = df1a['TransactionCounts'][2]
            st.write(f'#### {val2}')
            st.write('')
            val3 = df1a['TransactionCounts'][3]
            st.write(f'#### {val3}')
            st.write('')
            
            val4 = df1a['TransactionCounts'][4]
            st.write(f'#### {val4}')
            st.write('')
            
            val5 = df1a['TransactionCounts'][5]
            st.write(f'#### {val5}')
        
        #st.dataframe() ##values to be inserted
#### here third layer of data
bsb1, bsb2,bsb3,bsb4,bsb5,bsb6 = st.columns([2,1,1,1,2,2])
with bsb1:
    stname = [
    'Arunachal-Pradesh', 'Assam', 'Chandigarh', 'Karnataka', 'Manipur', 'Meghalaya', 
    'Mizoram', 'Nagaland', 'Punjab', 'Rajasthan', 'Sikkim', 'Tripura', 'Uttarakhand', 
    'Telangana', 'Bihar', 'Kerala', 'Madhya-Pradesh', 'Andaman-&-Nicobar-Islands', 'Gujarat', 
    'Lakshadweep', 'Odisha', 'Dadra-&-Nagar-Haveli-&-Daman-&-Diu', 'Ladakh', 
    'Jammu-&-Kashmir', 'Chhattisgarh', 'Delhi', 'Goa', 'Haryana', 'Himachal-Pradesh', 
    'Jharkhand', 'Tamil-Nadu', 'Uttar-Pradesh', 'West-Bengal', 'Andhra-Pradesh', 
    'Puducherry', 'Maharashtra'
]
    defk = stname.index("Tamil-Nadu")
    stnr = st.selectbox('',stname,key='stname',index=defk)
with bsb2:
    chgh = ['bar','line','area']
    chfk = chgh.index('line')
    fnch = st.selectbox('',chgh,key='ploti',index=chfk)
with bsb3:
    y1 = ['2018', '2019', '2020','2021','2022']
    default_y1 = y.index("2022")
    year1 = st.selectbox('',
            y1,key='year1',index=default_y1)

with bsb4:
    q1 = ['Q1', 'Q2', 'Q3','Q4']
    default_qua1 = q.index("Q1")
    qua1 = st.selectbox('',
            q1,key='quarter1',index=default_qua)
    if qua1 == 'Q1':
        quarter1 = 1
    elif qua1 == 'Q2':
        quarter1 = 2
    elif qua1 == 'Q3':
        quarter1 = 3
    elif qua1 == 'Q4':
        quarter1 = 4

with bsb5:
    ust1a = ["Users", "Transactions"]
    default_index1 = ust1a.index("Transactions")
    u_t1 = st.selectbox("", ust1a,key='u_t1',index=default_index1)

with bsb6:
    if u_t1 == "Transactions":
        usty1 = ["TransactionAmount","TransactionCount"]
        default_index2 = usty1.index("TransactionAmount")
        u_t2 = st.selectbox("", usty1,key='u_t2',index=default_index2)
    else:
        usty1a = ["NoOfUsers","NoOfAppOpens",]
        default_index2a = usty1a.index("NoOfUsers")
        u_t2a = st.selectbox("", usty1a,key='u_t2',index=default_index2a)

### shape of the invidual districts

url2 = 'https://github.com/pnraj/Projects/raw/master/Phonephe_Pulse/test.geojson'

response1 = requests.get(url2)
with open('test.geojson', 'wb') as file:
    file.write(response1.content)

india_states1 = gpd.read_file('test.geojson')
jk = india_states1.loc[india_states1['ST_NM'] == str(stnr), 'geometry']
# Plot the selected area using Geopandas' plot function
stfig, ax = plt.subplots(figsize=(90 / 10, 70 / 10))
jk.plot(ax=ax, facecolor='green', edgecolor='blue')
ax.axis('off') # Remove the axis ticks and labels
## data for line and other grahs
cha_df = users_df.copy()
cha_df['StateName']=cha_df['StateName'].apply(lambda x: x.title()) 
ch = cha_df.loc[(cha_df['Year']==int(year1)) & (cha_df['Quarter']==int(quarter1)) & (cha_df['StateName']==str(stnr))]
ch['DistrictName'] = ch['DistrictName'].apply(lambda x: x.title())
lnk = ch[['DistrictName','UsersCount']] ## userscounts
lnka = ch[['DistrictName','AppOpening']] ## Appopenings
### transaction chart data
transch_df = trans_df.copy()
transch_df['StateName']=transch_df['StateName'].apply(lambda x: x.title()) 
ch1 = transch_df.loc[(transch_df['Year']==int(year1)) & (transch_df['Quarter']==int(quarter1)) & (transch_df['StateName']==str(stnr))]
ch1['DistrictName']=ch1['DistrictName'].apply(lambda x: x.title())
lnk1 = ch1[['DistrictName','TotalTransactionAmount']] ## total transaction amount
lnk2 = ch1[['DistrictName','TotalTransactionCount']] ## total transaction count



# if-else statement for choosing a type of graph


c1,c2 = st.columns([3,6])
if u_t1 == "Users":
    with c1:
    # Display the plot in Streamlit
        st.write(f'### {str(stnr)}')
        st.pyplot(stfig)
    with c2:
        if u_t2a == "NoOfUsers":
            if fnch == 'line':
                st.write(str(stnr))
                figch = px.line(lnk, x='DistrictName', y='UsersCount',width=850, height=525)
                st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))
            elif fnch == 'bar':
                figch = px.bar(lnk, x='DistrictName', y='UsersCount',width=850, height=525)
                st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))
            elif fnch == 'area':
                figch = px.area(lnk, x='DistrictName', y='UsersCount',width=850, height=525)
                st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))
        else:
            if fnch == 'line':
                st.write(str(stnr))
                figch = px.line(lnka, x='DistrictName', y='AppOpening',width=850, height=525)
                st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))
            elif fnch == 'bar':
                figch = px.bar(lnka, x='DistrictName', y='AppOpening',width=850, height=525)
                st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))
            elif fnch == 'area':
                figch = px.area(lnka, x='DistrictName', y='AppOpening',width=850, height=525)
                st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))

    
else:
    with c1:
    # Display the plot in Streamlit
        st.write(f'### {str(stnr)}')
        st.pyplot(stfig)
    with c2:
        if u_t2 == "TransactionAmount":
            if fnch == 'line':
                
                figch = px.line(lnk1, x='DistrictName', y='TotalTransactionAmount',width=850, height=525)
                st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))
            elif fnch == 'bar':
                figch = px.bar(lnk1, x='DistrictName', y='TotalTransactionAmount',width=850, height=525)
                st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))
            elif fnch == 'area':
                figch = px.area(lnk1, x='DistrictName', y='TotalTransactionAmount',width=850, height=525)
                st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))
        else:
            if fnch == 'line':
                st.write(str(stnr))
                figch = px.line(lnk2, x='DistrictName', y='TotalTransactionCount',width=850, height=525)
                st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))
            elif fnch == 'bar':
                figch = px.bar(lnk2, x='DistrictName', y='TotalTransactionCount',width=850, height=525)
                st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))
            elif fnch == 'area':
                figch = px.area(lnk2, x='DistrictName', y='TotalTransactionCount',width=850, height=525)
                st.plotly_chart(figch, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))

### third layer
thc1,thc2,thc3,thc4 = st.columns([0.1,6,6,0.1])
with thc2:
    pth1a = ["TotalTransactionAmount","TotalTransactionCount","AppOpening","UsersCount"]
    pieind = pth1a.index("TotalTransactionAmount")
    piea1 = st.selectbox("", pth1a,key='pit',index=pieind)
with thc3:
    pth1b = ["TotalTransactionAmount","TotalTransactionCount","AppOpening","UsersCount"]
    pieind1 = pth1b.index("UsersCount")
    piea2 = st.selectbox("", pth1b,key='pit1',index=pieind1)


### Pie chart for Uerscount and total transaction count 

df = users_df.copy()
df1 = trans_df.copy()
mer_df = df.merge(df1,on=['DistrictName','StateName','Year','Quarter'],how='left')
df_sorted = mer_df.sort_values('Year')
# Create subplots with 1 row and 2 columns
piefig = sp.make_subplots(rows=1, cols=2, subplot_titles=(piea1, piea2), specs=[[{'type': 'pie'}, {'type': 'pie'}]])

# Add the first pie chart for registered users
piefig.add_trace(go.Pie(labels=df_sorted['Year'], values=df_sorted[piea1], hole=0.5,
                     hovertemplate=f"Year: %{{label}}<br>{piea1}: %{{value:,.0f}}"),
              row=1, col=1)

# Add the second pie chart for transactions
piefig.add_trace(go.Pie(labels=df_sorted['Year'], values=df_sorted[piea2], hole=0.5,
                    hovertemplate=f"Year: %{{label}}<br>{piea2}: %{{value:,.0f}}"),
              row=1, col=2)

# Update the layout
piefig.update_layout(height=600, width=1250)

# Show the chart
st.plotly_chart(piefig, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False, layout=dict({'width': '100%'}, **{'height': '100%'}))
