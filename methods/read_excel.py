import pandas as pd
from proj_consts import paths

def more_indices_folder_to_df(indices_list:list)->pd.DataFrame():
    """
    reads the files in folder (loop)
    adds the "Symbol" = file name suffix, as new column
    adjusts columns names and date type
    """
    files_folder = paths.cache #paths.new / "TA_Indices"   
    xls_files = [file for file in files_folder.glob("*.xls") if file.stem in indices_list]
    if not xls_files:
        return pd.DataFrame()
    df = pd.DataFrame()
    for file_path in xls_files:
        df_add=pd.read_excel(file_path,skiprows=6)
        first_null_row = df_add.isnull().any(axis=1).idxmax()
        df_add = df_add.iloc[:first_null_row]
        
        df_add["Symbol"]=file_path.stem
        df_add.columns=["Date","Close","Symbol"]
        df_add['Date']=pd.to_datetime(df_add['Date'], format='%Y-%m-%d')
        df_add.sort_values('Date',inplace=True)
        df_add.reset_index(inplace=True,drop=True)
        df=pd.concat([df,df_add])
    return df
    
def ta_indices_folder_to_df(indices_list:list)->pd.DataFrame():
    """
    reads the files in folder (loop)
    adds the "Symbol" = file name suffix, as new column
    adjusts columns names and date type
    """
    files_folder = paths.cache
    csv_files = [file for file in files_folder.glob("*.csv") if file.stem in indices_list]
    if not csv_files:
        return pd.DataFrame()
    df = pd.DataFrame()
    for file_path in csv_files:
        df_add=pd.read_csv(file_path,header=1)
        df_add["Symbol"]=file_path.stem.removeprefix("ChartData-")
        df_add.columns=["Date","Close","Cycle","Symbol"]
        df_add['Date']=pd.to_datetime(df_add['Date'], format='%d/%m/%Y')
        df_add.sort_values('Date',inplace=True)
        df_add.reset_index(inplace=True,drop=True)
        df=pd.concat([df,df_add])
    return df

def fabricate_gemel_data():
    #required columns: Date,Symbol,Close
    gemel_data_path=paths.new / "Gemel_data.xlsx"
    gemel_data=pd.read_excel(gemel_data_path)
    gemel_data['Date']=pd.to_datetime(gemel_data['year'], format='%Y')
    
    gemel_data=close_field(gemel_data)
    return gemel_data

def cum_revenue(group:pd.DataFrame)->pd.DataFrame:
    group.reset_index(inplace=True,drop=True)
    for i, row in group.iterrows():
        if i==0:
            group.loc[i,"Close"]=1+row["Revenue"]
        else:
            group.loc[i,"Close"]=group.loc[i-1,"Close"]*(1+row["Revenue"])
    return group

def close_field(gemel_data:pd.DataFrame)->pd.DataFrame:
    g_gemel_data=gemel_data.groupby("Symbol")
    new_gemel_data=pd.DataFrame()
    
    for name, group in g_gemel_data:
        add=cum_revenue(group)
        new_gemel_data=pd.concat([new_gemel_data,add])
    return new_gemel_data