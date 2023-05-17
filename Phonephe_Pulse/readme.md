#  PhonePe Pulse Data Analysis 2018-2022  _[Dashboard](https://pnraj-projects-phonephe-pulsedashboard-y5wmx8.streamlit.app)_
## Project Requirments:
- __[Python 3.11](https://www.google.com/search?q=docs.python.org)__ 
- __[Pandas](https://www.google.com/search?q=python+pandas)__
- __[Streamlit](https://www.google.com/search?q=python+streamlit)__
- __[Plotly](https://www.google.com/search?q=python+plotly)__
- __[Matplotlib](https://www.google.com/search?q=python+matplotlib)__
- __[Geopandas](https://www.google.com/search?q=python+geopandas)__
- __[Requests](https://www.google.com/search?q=python+requests)__

## General workflow of this Project:
![PhonePe Design](https://github.com/pnraj/Projects/assets/29162796/b97ce7b9-634a-4612-bef7-77369b4a89c6)
## Dashboard Preview
<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/d183e86b-4d47-4b3a-906f-bb20ea3de9a6" alt="Description of the image">
</p>
      
### PhonePe Pulse Dashboard contains three section:

1.__Overall Geo visualization:__
   
   * PhonePe Pulse `Geo visulization` includes two options __Users Count and Transaction Amount__  in __INDIA__ from __2018 To 2022__
     
   * Every States in INDIA are ploted in map using Plotly `choropleth_mapbox` based upon scale of values the ratio os colour scale will differs
   
   * __Users__ can use three `Drop Down` button on top right corner to view different options to choose from __Year, Quarter, Transaction or Users__
   
   * Under the __Users__ `Drop Down` contains _No of Users_ and _No of App Opens_ in _Each Quarter_ of _Every Year_ with **Top 10 Districts, States, Pincode wise Sorted values**
   
   * Under the __Transaction__ `Drop Down` contains _Total Transaction Counts, Transaction Amounts, Averge of Transactions_ with __Mode of Transactions__ 

2.__District wise Visualization:__

   * This Section Gives Detailed Analysis of __Users__ and their __Transaction__ in Each __Indian States__ and their __Districts__
   
   * There are Six `Drop Down` Buttons __State Name, Type Of Graph, Year, Quarter, Users or Transaction, Users count/Appopens or TransactionAmount/TransactionCount__
   
   * Each States in India is displayed in `left side` of this section using __Matplotlib Subplot__ and their Disticts Visualization in `right side` using __Plotly Express__
   
3.__Year Wise Visualization:__ 

   * This Section Gives Detailed Analysis of __Users__ and __Transaction__ over the years from __2018 to 2022__ using `plotly.graph_objects` __Pie Chart__
   
   * There are Two `Drop Down` Buttons __Users Count, AppOpens, Transaction Amount and Transaction Count__
     
### The Files in the repo and How they are used in this app
      
- `dashboard.py` is the Phonepe dashboard app which is built on top off __Streamlit__
```py
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
```

- `data/db.py` is the `sqlite3` file mainly used to query the data from `phonepe.db` file and convert them into `pandas dataframe`
``` py
          url = 'https://raw.githubusercontent.com/pnraj/Projects/master/Phonephe_Pulse/data/phonphe.db'
          db_file = wget.download(url)
          conn = sqlite3.connect(db_file)

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
 ```
> `Data_Preprocessing/db.py` can be used if you want to connect with your `mysql database` which you loaded the Processed PhonePe data  

- `geojson` files in `data/` is used for ploting the values
```py 
      url = 'https://github.com/pnraj/Projects/raw/master/Phonephe_Pulse/data/states_india.geojson'
      response = requests.get(url)
      with open('states_india.geojson', 'wb') as file:
          file.write(response.content)
      india_states = json.load(open('states_india.geojson', "r"))
      ## For values refer the dashboard.py
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
        
```
   


