#  <a href="https://pnraj-projects-phonephe-pulsedashboard-y5wmx8.streamlit.app/" target="_blank"> PhonePe Pulse Data Analysis 2018-2022 Dashboard </a>
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
      
- `dashboard.py` is the Phonepe dashboard app which is built on top off __Streamlit__, 
- 

- `data/db.py` is the `sqlite3` file mainly used to query the data from `phonepe.db` file and convert them into `pandas dataframe`
> `Data_Preprocessing/db.py` can be used if you want to connect with your `mysql database` which you loaded the Processed PhonePe data  
- 
   


