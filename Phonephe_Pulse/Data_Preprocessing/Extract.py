# Extraction or Transformation of file from directory(PhonePhe)
import pandas as pd
import os
from pathlib import Path

class agg_tran:
    def __init__(self, agg_tran_path):
        self.state_aggregated_transaction = pd.DataFrame({})
        self.agg_tran_path = agg_tran_path
    
    
    def aggregated_transaction(self,state, year, quarter, path):
        
        a_dft = pd.read_json(path) # dataframe
        # data sorting
        trs_df = a_dft.data.transactionData
        if trs_df:
            for i in trs_df:
                all_rows = {"Transaction_method":i['name'],"Transaction_Counts":i['paymentInstruments'][0]['count'],"Transaction_amounts":i['paymentInstruments'][0]['amount'],"state":state,"year":year,"quarter":quarter}
                all_rows_df = pd.DataFrame.from_dict([all_rows])
                self.state_aggregated_transaction = pd.concat([self.state_aggregated_transaction,all_rows_df])
                self.state_aggregated_transaction['Transaction_amounts'] = self.state_aggregated_transaction['Transaction_amounts'].apply(lambda x: int(x))
            self.state_aggregated_transaction.reset_index(drop=True, inplace=True)
    def extract_data(self):
            for state in os.listdir(self.agg_tran_path):
                state_path = os.path.join(self.agg_tran_path, state)

                for year in range(2018, 2023):
                    year_path = os.path.join(state_path, str(year))
                    qfiles = []

                    for (dirpath, dirnames, filenames) in os.walk(year_path):
                        qfiles.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.json')])
                        break

                    for qfile_path in qfiles:
                        quarter = Path(qfile_path).stem
                        self.aggregated_transaction(state, year, quarter, qfile_path)
            return self.state_aggregated_transaction



class agg_users:
    def __init__(self,agg_usr_path):
        self.state_aggregated_users = pd.DataFrame({})
        self.agg_usr_path = agg_usr_path
    
    def aggregated_users(self,state, year, quarter, path):
        
        u_dft = pd.read_json(path) # dataframe
        # data sorting
        reg_users = u_dft['data']['aggregated']['registeredUsers']
        app_opens = u_dft['data']['aggregated']['appOpens']
        
        urs_df = u_dft.data.usersByDevice
        if urs_df:
            for i in urs_df:
                all_rows = {"Device_Brand":i['brand'],"Brand_count":i['count'],"percentage":i['percentage'],"Registered_users":reg_users,"App_opening":app_opens,"state":state,"year":year,"quarter":quarter}
                all_rows_df = pd.DataFrame.from_dict([all_rows])
                self.state_aggregated_users = pd.concat([self.state_aggregated_users,all_rows_df])
            self.state_aggregated_users.reset_index(drop=True, inplace=True)
    
    def extract_data(self):
            for state in os.listdir(self.agg_usr_path):
                state_path = os.path.join(self.agg_usr_path, state)

                for year in range(2018, 2023):
                    year_path = os.path.join(state_path, str(year))
                    qfiles = []

                    for (dirpath, dirnames, filenames) in os.walk(year_path):
                        qfiles.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.json')])
                        break

                    for qfile_path in qfiles:
                        quarter = Path(qfile_path).stem
                        self.aggregated_users(state, year, quarter, qfile_path)
            return self.state_aggregated_users 

class map_tran:
    def __init__(self,map_tran_path):
        self.state_map_transaction = pd.DataFrame({})
        self.map_tran_path = map_tran_path
    
    def map_transaction(self,state, year, quarter, path):
       
        m_dft = pd.read_json(path) # dataframe
        # data sorting
        map_dft = m_dft.data.hoverDataList
        
        if map_dft:
            for i in map_dft:
                all_rows = {"Distric_Name":i['name'],"Total_Transaction_count":i['metric'][0]['count'],"Total_Transaction_amount":i['metric'][0]['amount'],"state":state,"year":year,"quarter":quarter}
                all_rows_df = pd.DataFrame.from_dict([all_rows])
                self.state_map_transaction = pd.concat([self.state_map_transaction,all_rows_df])
                self.state_map_transaction['Total_Transaction_amount'] = self.state_map_transaction['Total_Transaction_amount'].apply(lambda x: int(x))
            self.state_map_transaction.reset_index(drop=True, inplace=True)

    def extract_data(self):
            for state in os.listdir(self.map_tran_path):
                state_path = os.path.join(self.map_tran_path, state)

                for year in range(2018, 2023):
                    year_path = os.path.join(state_path, str(year))
                    qfiles = []

                    for (dirpath, dirnames, filenames) in os.walk(year_path):
                        qfiles.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.json')])
                        break

                    for qfile_path in qfiles:
                        quarter = Path(qfile_path).stem
                        self.map_transaction(state, year, quarter, qfile_path)
            return self.state_map_transaction

class map_usr:
    
    def __init__(self,map_usr_path):
        self.state_map_users = pd.DataFrame({})
        self.map_usr_path = map_usr_path
    
    def map_users(self,state, year, quarter, path):
        
        m_dft = pd.read_json(path) # dataframe
        # data sorting
        map_dft = m_dft.data.hoverData
        
        if map_dft:
            for i in map_dft:
                all_rows = {"Distric_Name":i,"Registered_users":map_dft[i]['registeredUsers'],"App_opening":map_dft[i]['appOpens'],"state":state,"year":year,"quarter":quarter}
                all_rows_df = pd.DataFrame.from_dict([all_rows])
                self.state_map_users = pd.concat([self.state_map_users,all_rows_df])
            self.state_map_users.reset_index(drop=True, inplace=True)
    
    def extract_data(self):
            for state in os.listdir(self.map_usr_path):
                state_path = os.path.join(self.map_usr_path, state)

                for year in range(2018, 2023):
                    year_path = os.path.join(state_path, str(year))
                    qfiles = []

                    for (dirpath, dirnames, filenames) in os.walk(year_path):
                        qfiles.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.json')])
                        break

                    for qfile_path in qfiles:
                        quarter = Path(qfile_path).stem
                        self.map_users(state, year, quarter, qfile_path)
            return self.state_map_users

class pin_users:
    def __init__(self,usr_pin_path):
        self.state_pin_users = pd.DataFrame({})
        self.usr_pin_path = usr_pin_path
    
    def agg_pin_users(self,state, year, quarter, path):
        
        p_dft = pd.read_json(path) # dataframe
        # data sorting
        pincodes = p_dft['data']['pincodes']
        districts = p_dft['data']['districts']
        
        if not p_dft.empty:
            for i in pincodes:
                all_rows = {"Pincodes":i['name'],"Total_Registered_users":i['registeredUsers'],"state":state,"year":year,"quarter":quarter}
                all_rows_df = pd.DataFrame.from_dict([all_rows])
                self.state_pin_users = pd.concat([self.state_pin_users,all_rows_df])
            self.state_pin_users.reset_index(drop=True, inplace=True)
            
            
    
    def extract_data(self):
            for state in os.listdir(self.usr_pin_path):
                state_path = os.path.join(self.usr_pin_path, state)

                for year in range(2018, 2023):
                    year_path = os.path.join(state_path, str(year))
                    qfiles = []

                    for (dirpath, dirnames, filenames) in os.walk(year_path):
                        qfiles.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.json')])
                        break

                    for qfile_path in qfiles:
                        quarter = Path(qfile_path).stem
                        self.agg_pin_users(state, year, quarter, qfile_path)
            return self.state_pin_users
                



def all_df(agg_usr_path,agg_tran_path,usr_pin_path,map_tran_path,map_usr_path):
    a = agg_tran(agg_tran_path)
    aggregateds_transaction = a.extract_data()
    b = agg_users(agg_usr_path)
    aggregateds_users = b.extract_data()
    c = map_tran(map_tran_path)
    maps_transaction = c.extract_data()
    d = map_usr(map_usr_path)
    maps_users = d.extract_data()
    e=pin_users(usr_pin_path)
    pincode_values = e.extract_data()
    return aggregateds_transaction, aggregateds_users, maps_transaction, maps_users,pincode_values

