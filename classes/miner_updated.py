import pandas as pd
from typing import Optional
import time
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

from methods import read_excel
from proj_consts import paths
from proj_consts.consts import LEVERAGED_ETF_MAPPING_CSV, LEVERAGED_ETF_MAPPING

def calculate_leveraged_etfs(stocks_df, etf_name):
    index_symbol = LEVERAGED_ETF_MAPPING[etf_name]
    index_data = (
        stocks_df[stocks_df["Symbol"] == index_symbol]
        if len(stocks_df[stocks_df["Symbol"] == index_symbol])
        else yfinance_handling([index_symbol])
    )
    # Analyze the leveraged ETF and append results to stocks_df
    lev_etf_data = analyze_leveraged_etf(index_data, etf_name)
    stocks_df = pd.concat([stocks_df, lev_etf_data], axis=0)

    return stocks_df
    
def old_calculate_leveraged_etfs(stocks_df, ticker):
    # Mapping of leveraged ETF descriptions to their underlying indices

    for etf_name, index_symbol in LEVERAGED_ETF_MAPPING.items():
        if etf_name in dfn.symbols:
            # Check if the index data is already available
            index_data = (
                stocks_df[stocks_df["Symbol"] == index_symbol]
                if index_symbol in dfn.symbols
                else yfinance_handling([index_symbol])
            )

            # Analyze the leveraged ETF and append results to stocks_df
            lev_etf_data = analyze_leveraged_etf(index_data, etf_name)
            stocks_df = pd.concat([stocks_df, lev_etf_data], axis=0)

    return stocks_df

def get_tase():
    # header = pd.read_csv(paths.new / "ChartData.csv",nrows=1)
    chart = pd.read_csv(paths.new / "ChartData.csv",skiprows=1)
    chart.columns = ["Date","Close","cycle"]
    chart["Date"] = pd.to_datetime(chart["Date"],format="%d/%m/%Y")
    chart["Symbol"] = "NADLAN"
    chart.drop(columns=["cycle"], inplace = True)
    return chart

def mine(dfn_import, source: Optional[str]="yfinance"):
    global dfn
    dfn = dfn_import

    start = time.perf_counter()
    stocks_df = pd.DataFrame()
    if source=="yfinance":
        stocks_df = yfinance_handling(dfn.symbols)
        # if "NADLAN" in dfn.symbols:
        #     tase = get_tase()
        #     stocks_df = pd.concat([stocks_df,tase],ignore_index=True)
    elif source=="gemel":
        stocks_df = read_excel.fabricate_gemel_data()
    elif source=="more_indices":
        stocks_df = read_excel.more_indices_folder_to_df(dfn.symbols)
    elif source=="ta_indices":
        stocks_df = read_excel.ta_indices_folder_to_df(dfn.symbols)
        for ticker in dfn.symbols:
            if ticker in LEVERAGED_ETF_MAPPING_CSV.keys():
                dfn.logger.debug(f"{ticker} is leveraged")
                lev_symbol = LEVERAGED_ETF_MAPPING_CSV[ticker]
                t_data = stocks_df[stocks_df["Symbol"]==lev_symbol] if lev_symbol in dfn.symbols else\
                    read_excel.ta_indices_folder_to_df([lev_symbol])
                lev = analyze_leveraged_etf(t_data, ticker)
                stocks_df = pd.concat([stocks_df,lev],axis=0)

    end = time.perf_counter()
    dfn.logger.info(f"\ntime to run Miner {end - start:.2f} seconds")
    return stocks_df

def yfinance_handling(tickers):
    # Path to cache file
    cache_path = paths.cache / "cache_tickers_history.pkl"
    today = datetime.today().date()
    # Initialize list for new data
    all_data = []

    if cache_path.exists():
        dfn.logger.debug("cache_tickers_history.pkl exists")
        # Load cached data
        cached_data = pd.read_pickle(cache_path)
        
        
        for ticker in tickers:
            # Filter for the specific ticker
            ticker_data = cached_data[cached_data['Symbol'] == ticker]
            
            # Determine the latest date for this ticker
            if not ticker_data.empty:
                dfn.logger.debug(f"cache for {ticker} exists")
                latest_date = ticker_data['Date'].max()
                latest_date = pd.to_datetime(latest_date).date()
            else:
                dfn.logger.debug(f"no cache for {ticker} exists")
                latest_date = None
            
            if latest_date is None or latest_date < today - timedelta(days=1):
                dfn.logger.debug(f"updating cache for {ticker} to today")
                # Download missing data for this ticker
                missing_start = (latest_date + timedelta(days=1)).strftime('%Y-%m-%d') if latest_date else None#dfn.start
                missing_end = today.strftime('%Y-%m-%d')
                
                # Process new data
                if ticker in LEVERAGED_ETF_MAPPING.keys():
                    dfn.logger.debug(f"{ticker} is leveraged")
                    new_data = calculate_leveraged_etfs(ticker_data, ticker)
                else:
                    new_data = yf.download(ticker, start=missing_start, end=missing_end)
                    new_data = yf_multi_stocks_handling(new_data, [ticker])
                # Append to new data
                all_data.append(new_data)
                dfn.logger.debug(f"{len(new_data)} new rows appended")
            
            # Keep existing data for this ticker
            if not ticker_data.empty:
                # import streamlit as st
                # st.write(dfn.start)
                # st.write(dfn.end)
                start = datetime.strptime(dfn.start, "%Y-%m-%d")
                end = datetime.strptime(dfn.end, "%Y-%m-%d")
                all_data.append(ticker_data.query("Date >= @start and Date <= @end"))
            
        # Combine all data and remove duplicates
        stocks_df = pd.concat(all_data).drop_duplicates().reset_index(drop=True)
        
        # Save updated data to cache
        stocks_df.to_pickle(cache_path)
    else:
        dfn.logger.debug("No cache, download all data")
        # No cache, download all data
        # stocks_df = yf.download(tickers, start=dfn.start, end=dfn.end)
        # stocks_df = yf_multi_stocks_handling(stocks_df, tickers)
        ticker_data = pd.DataFrame({"Symbol": []})
    
        for ticker in tickers:
            if ticker in LEVERAGED_ETF_MAPPING.keys():
                dfn.logger.debug(f"{ticker} is leveraged")
                new_data = calculate_leveraged_etfs(ticker_data, ticker)
            else:
                new_data = yf.download(ticker, start=dfn.start, end=dfn.end)
                new_data = yf_multi_stocks_handling(new_data, [ticker])
            # Append to new data
            all_data.append(new_data)
            dfn.logger.debug(f"{len(new_data)} new rows appended")
        # Combine all data and remove duplicates
        stocks_df = pd.concat(all_data).drop_duplicates().reset_index(drop=True)


        # Save to cache
        # stocks_df.to_pickle(cache_path)

    return stocks_df

def yf_multi_stocks_handling(stocks_df, tickers)->pd.DataFrame:
    a = stocks_df.copy()
    if isinstance(a.columns, pd.MultiIndex):
        ix=a.columns.droplevel(1).str.match("Close")
    else:
        ix=a.columns.str.match("Close")
        
    b=a.loc[:,ix]#keep only Close value columns
    
    if isinstance(a.columns, pd.MultiIndex):
        b.columns=b.columns.droplevel(0)#rename columns to stock symbols
    else:
        b.columns = tickers

    c=b.melt(value_vars=b.columns,var_name="Symbol", 
                          value_name='Close',ignore_index=False)
    stocks_df=c.reset_index()
    # import numpy as np
    # stocks_df.replace(0, np.nan, inplace=True)
    # stocks_df.dropna()
    return stocks_df

def analyze_leveraged_etf(prices_df, name="3X Leveraged S&P",leverage=3.0,
                           expense_ratio=0.0095,initial_price=100):
    """
    Analyze leveraged ETF performance and decay effects
    
    Parameters:
    prices_df: DataFrame with 'Date' and 'Close' columns
    leverage: leverage multiplier (default 3.0)
    expense_ratio: annual expense ratio (default 0.95% which is typical for leveraged ETFs)
    #0.0095
    Returns:
    Dictionary containing analysis results
    """
    if name == "3X Leveraged TA-125" or name == "3X Leveraged TA-35":
        expense_ratio=0.0229
    elif name == "2X Leveraged Nifty50":
        leverage=2.0
    elif name == "2X Leveraged ETH":
        leverage=2.0
        expense_ratio=0.0094
    elif name == "2X Leveraged BTC":
        leverage=2.0
        expense_ratio=0.0185
    elif name == "2X Leveraged Silver":
        leverage=2.0
        expense_ratio=0.0095
    elif name == "2X Leveraged Gold":
        leverage=2.0
        expense_ratio=0.0095
    # Calculate daily returns
    df = prices_df.copy()
    df['Daily_Return'] = df['Close'].pct_change()
    
    # Calculate proper daily expense ratio using compound interest formula
    daily_expense_ratio = (1 + expense_ratio)**(1/252) - 1

    # Calculate leveraged returns (before fees)
    df['Leveraged_Return'] = (df['Daily_Return'] * leverage) - daily_expense_ratio  # Daily expense ratio
    # Vectorized cumulative product for price calculation
    df['Leveraged_Close'] = initial_price * (1 + df['Leveraged_Return']).cumprod()
    
    # Fill the first NaN value with initial price
    df['Leveraged_Close'].iloc[0] = initial_price
    
    prices_df['Close'] = df['Leveraged_Close']
    prices_df['Symbol'] = name

    # Calculate cumulative returns
    # df['Base_Cumulative'] = (1 + df['Daily_Return']).cumprod()
    # df['Leveraged_Cumulative'] = (1 + df['Leveraged_Return']).cumprod()
    return prices_df
