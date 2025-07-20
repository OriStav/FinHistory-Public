import pandas as pd
import yfinance as yf
# import logging
from typing import Optional
import time

from methods import read_excel


LEVERAGED_ETF_MAPPING = {
        "3X Leveraged TA-Banks": "TA-BANKS",
        "3X Leveraged S&P": "^GSPC",
        "3X Leveraged Nasdaq": "^NDX",
        "3X Leveraged Russel": "^RUT",
        # "3X Leveraged S&P": "SPY",
        "3X Leveraged Nasdaq": "^NDX",
        "2X Leveraged Nifty50": "^NSEI",
        "3X Leveraged TA-125": "^TA125.TA",
        "3X Leveraged TA-35": "TA35.TA",
        "3X Leveraged BTC": "BTC-USD",
        "2X Leveraged BTC": "BTC-USD",
        "2X Leveraged ETH": "ETH-USD",
        "2X Leveraged Gold": "GC=F",
        "2X Leveraged Silver": "SI=F",
    }

def mine(dfn_import,source: Optional[str]="yfinance"):
    global dfn
    dfn = dfn_import

    start = time.perf_counter()
    stocks_df=pd.DataFrame()
    # self.logger=Text._logger_
    if source=="yfinance":
        stocks_df = yfinance_handling(dfn.symbols)
        if "3X Leveraged S&P" in dfn.symbols:
            gspc = stocks_df[stocks_df["Symbol"]=="^GSPC"] if "^GSPC" in dfn.symbols else yfinance_handling(["^GSPC"])
            lev = analyze_leveraged_etf(gspc,"3X Leveraged S&P")
            stocks_df = pd.concat([stocks_df,lev],axis=0)
        if "3X Leveraged TA" in dfn.symbols:
            gspc = stocks_df[stocks_df["Symbol"]=="TA35.TA"] if "TA35.TA" in dfn.symbols else yfinance_handling(["TA35.TA"])
            lev = analyze_leveraged_etf(gspc,"3X Leveraged TA")
            stocks_df = pd.concat([stocks_df,lev],axis=0)
        if "3X Leveraged Nasdaq" in dfn.symbols:
            ndx = stocks_df[stocks_df["Symbol"]=="^NDX"] if "^NDX" in dfn.symbols else yfinance_handling(["^NDX"])
            ndx_lev = analyze_leveraged_etf(ndx,"3X Leveraged Nasdaq")
            stocks_df = pd.concat([stocks_df,ndx_lev],axis=0)
    elif source=="gemel":
        stocks_df = read_excel.fabricate_gemel_data()
    elif source=="more_indices":
        stocks_df = read_excel.more_indices_folder_to_df(dfn.symbols)
    elif source=="ta_indices":
        stocks_df = read_excel.ta_indices_folder_to_df(dfn.symbols)
        if "3X Leveraged TA-Banks" in dfn.symbols:
            banks = stocks_df[stocks_df["Symbol"]=="TA-BANKS"] if "TA-BANKS" in dfn.symbols else\
                 read_excel.ta_indices_folder_to_df(['TA-BANKS'])
            lev = analyze_leveraged_etf(banks,"3X Leveraged TA-Banks")
            stocks_df = pd.concat([stocks_df,lev],axis=0)
    end = time.perf_counter()
    dfn.logger.info(f"\ntime to run Miner {end - start:.2f} seconds")
    return stocks_df

def yfinance_handling(tickers):
    stocks_df = yf.download(tickers,start=dfn.start, end=dfn.end)
    stocks_df = yf_multi_stocks_handling(stocks_df, tickers)
    # self.stocks_df.to_csv(Path("DB/Inputs/stocks_data.csv"),
                 # index = False, header = False, mode='a')
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
    return stocks_df

def analyze_leveraged_etf(prices_df, name="3X Leveraged S&P",leverage=3.0,
                           expense_ratio=0.0095,initial_price=100):
    """
    Analyze leveraged ETF performance and decay effects
    
    Parameters:
    prices_df: DataFrame with 'Date' and 'Close' columns
    leverage: leverage multiplier (default 3.0)
    expense_ratio: annual expense ratio (default 0.95% which is typical for leveraged ETFs)
    
    Returns:
    Dictionary containing analysis results
    """
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
