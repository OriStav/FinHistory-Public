import streamlit as st

COL_CONFIG = {"Symbol": st.column_config.TextColumn("🪙 Asset",width="medium"),
              "duration_round": st.column_config.NumberColumn("⏱️ Investment Duration",format="%.0f",width="medium"),
              "average_actual_duration": st.column_config.NumberColumn("📊 Avg Actual Duration",format="%.1f",width="medium"),
              "std_actual_duration": st.column_config.NumberColumn("📈 Std Actual Duration",format="%.2f",width="medium"),
              "withdrawal_date": st.column_config.DatetimeColumn("📅 Withdrawal Date",format="DD/MM/YYYY",width="medium"),
              "current_percentile": st.column_config.NumberColumn("📊 Current Percentile",format="%.1f%%",width="medium"),
              "yearly_profit_percentage": st.column_config.NumberColumn("💰 Annualized Profit %",format="%.1f%%",width="medium")}

COL_CONFIG_WEIGHTS={
            "Weight": st.column_config.NumberColumn(
                "Weight",
                help="Portfolio weight assigned to this ticker"
            ),
            "Weight %": st.column_config.NumberColumn(
                "Weight %",
                help="Percentage of total portfolio weight",
                format="%.1f%%"
            ),
            "Median Return [%]": st.column_config.NumberColumn(
                "Median Return [%]",
                help="Median annualized return across all investment durations"
            ),
            "Std Dev [%]": st.column_config.NumberColumn(
                "Std Dev [%]",
                help="Standard deviation of annualized returns"
            ),
            "Mean Return [%]": st.column_config.NumberColumn(
                "Mean Return [%]",
                help="Average annualized return across all investment durations"
            ),
            "Min Return [%]": st.column_config.NumberColumn(
                "Min Return [%]",
                help="Minimum annualized return observed"
            ),
            "Max Return [%]": st.column_config.NumberColumn(
                "Max Return [%]",
                help="Maximum annualized return observed"
            ),
            "Sample Count": st.column_config.NumberColumn(
                "Sample Count",
                help="Number of investment simulations for this ticker"
            )
        }


LEVERAGED_ETF_MAPPING_CSV = {
        "3X Leveraged TA-Banks": "TA-BANKS.TA",
        "3X Leveraged NADLAN": "ESTATE15.TA",
    }
LEVERAGED_ETF_MAPPING = {
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

TICKERS = {
    "TCEHY": "US Inverse", "BABA": "US Inverse", "KWEB": "US Inverse", "GOOGL": "TopUS", "AAPL": "TopUS", "AMZN": "TopUS", "NFLX": "TopUS", "BRK-B": "TopUS", "GSPC": "TopUS", 
    "META": "TopUS", "WYNN": "TopUS", "GIS": "TopUS",  "^RUT": "TopIndices", "^DJI": "TopIndices", "^FTSE": "TopIndices", "^GDAXI": "TopIndices", "TA35.TA": "TopIndices", 
    "TA90.TA": "TopIndices", "^N225": "TopIndices", "^HSI": "TopIndices", "^NSEI": "TopIndices", "^STOXX": "TopIndices", "^SOXX": "TopIndices", "ACWI": "TopIndices", "IEMG": "TopIndices", "URTH": "TopIndices", 
    "SWRD.L": "TopIndices", "SSO": "TopIndices", "UPRO": "TopIndices", "STRS.TA": "TA", "SPEN.TA": "TA", "ELTR.TA": "TA", "VTNA.TA": "TA", "NICE.TA": "TA",
    "ICL.TA": "TA", "PHOE.TA": "TA", "FIBI.TA": "TA", "ORA.TA": "TA", "AZRG.TA": "TA", "GLTC.TA": "TA", "GLRS.TA": "TA", 
    "IMCO.TA": "TA", "ISCD.TA": "TA", "ISCN.TA": "TA", "MNRT.TA": "TA", "MNRA.TA": "TA", "ESTATE15.TA": "TA", 
    "MVNE.TA": "TA", "MLSR.TA": "TA", "RIT1.TA": "TA", "AMOT.TA": "TA", "ASHO.TA": "TA", "IBM": "Predictive", "SAP": "Predictive", "SIEGY": "Predictive", 
    "MSFT": "Predictive", "GE": "Predictive", "INTC": "Predictive", "BOSCHLTD.BO": "Predictive", "BOSCHLTD.NS": "Predictive", "SAP": "Predictive", "MSFT": "Predictive", "AI": "Predictive", 
    "XAO.AX": "Aussie", "IBIT": "Crypto", "SOS": "Crypto Miners", "RIOT": "Crypto Miners", "BITF": "Crypto Miners", "MARA": "Crypto Miners", "HUT": "Crypto Miners", "CMS": "Data Centers", "FSLR": "Data Centers", "GOOGL": "Data Centers", 
    "AMZN": "Data Centers", "VRT": "Data Centers", "NOK": "Loser", "CARR": "HVACR", "CC": "HVACR", "TT": "HVACR", "JCI": "HVACR", "DKILY": "HVACR", "005930.KS": "HVACR", "DNZOY": "HVACR", 
    "VLEEY": "HVACR", "018880.KS": "Automotive_HVAC", "GOOGL": "Automotive_HVAC", "INTC": "Automotive_HVAC", "GIS": "Hippie", "GS": "Hippie", "AAPL": "Hippie", "NKE": "Hippie", "HITI.V": "Hippie", 
    "TXN": "Hippie", "TSM": "Hippie", "SWK": "Hardware", "UFPI": "Hardware", "CENT": "Hardware", "HD": "Hardware", "NICE.TA": "Hardware", "MLSR.TA": "Hardware", "AZRG.TA": "FocusTA", 
    "SPEN.TA": "FocusTA", "VTNA.TA": "FocusTA", "RIT1.TA": "FocusTA", "META": "FocusTA", "TSLA": "FocusTA", "BABA": "FocusTA", "TCEHY": "FocusTA", "KWEB": "Focus5", 
    "BTC-USD": "Focus5", "005930.KS": "Focus4", "EADSY": "Focus4", "GOOGL": "Focus4", "NKE": "Focus4", "BOSCHLTD.BO": "Focus4", "CRM": "Focus3", "ORCL": "Focus3", 
    "ADBE": "Focus3", "HD": "Focus3", "DKILY": "Focus3", "018880.KS": "Focus2", "BRK-B": "Focus2", "AAPL": "Focus2", "AMZN": "Focus2", "NFLX": "Focus2", "EVTL": "Focus1", 
    "VTNA.TA": "Focus1", "LILM": "Focus1", "QS": "Focus1", "TSLA": "Focus1", "TM": "EVTOL", "TOYOF": "EVTOL", "EADSY": "EVTOL", "FCEL": "Energy", "BLDP": "Energy", "PLUG": "Energy", 
    "CVX": "Energy", "ILS=X": "Energy", "BTC-USD": "Energy", "DOGE-USD": "Energy", "CRM": "Energy", "ZEN": "Energy", "HUBS": "Energy", "ORCL": "Energy", "ADBE": "Energy", 
    "GC=F": "Commodities", "IGRO.AX": "Aussie", "IBAL.AX": "Aussie", "IXI.AX": "Aussie", "VAS.AX": "Aussie", "ASX.AX": "Aussie", "IRM": "Data Centers", "EQIX": "Data Centers", 
    "DLR": "Data Centers", "SRVR": "Data Centers", "VPN": "Data Centers", "VPU": "Energy", "OPC.HM": "MoneyMarket", "GSY": "MoneyMarket", "PULS": "MoneyMarket", "SLQD": "MoneyMarket", "IGSB": "MoneyMarket", "IGRO.AX": "Nov24AUD", 
    "IBAL.AX": "Nov24AUD", "IXI.AX": "Nov24AUD", "VAS.AX": "Nov24AUD", "ASX.AX": "Nov24AUD", "URTH": "Nov24AUD", "XAO.AX": "Nov24AUD", "RUT": "Nov24ILS", "GC=F": "Nov24ILS", "NSEI": "Nov24ILS", 
    "AFHL.TA": "Nov24USD", "SKBNF.TA": "Nov24USD", "INTC": "Nov24USD", "WYNN": "Nov24USD", "TSLA": "Nov24USD", "GIS": "Nov24USD", "ORCL": "Nov24USD", "COST": "Nov24USD", "OPC.HM": "Nov24USD", 
    "VUG": "Nov24USD", "ADM": "Nov24USD", "SARK": "Nov24USD", "AFHL.TA": "Nov24USD", "SKBNF.TA": "Nov24USD", "VUG": "Nov24USD", "VOOG": "Nov24USD", "CPI": "Nov24USD", "COST": "Nov24USD", 
    "ADM": "Nov24USD", "SARK": "Nov24USD", "VGS.AX": "TopIndices", "VGS.AX": "TopIndices", "SWRD.L": "TopIndices", "URTH": "TopIndices", "RUT": "TopIndices", "NSEI": "TopIndices", "AFHL.TA": "TopUS", 
    "BTC-USD": "TopUS", "DOGE-USD": "US Inverse", "ASX.AX": "Aussie", "IXI.AX": "World", "IGRO.AX": "World", "VGS.AX": "World", "GOOGL": "World", 
    "AMZN": "Nov24", "EQIX": "Nov24", "INTC": "Nov24", "TSLA": "Nov24", "GIS": "Nov24", "ADM": "Nov24", "RIOT": "Nov24"
}

STOCKS = list(set(list(LEVERAGED_ETF_MAPPING.keys()) + \
    list(LEVERAGED_ETF_MAPPING_CSV.keys()) + \
    list(LEVERAGED_ETF_MAPPING.values()) + \
    list(LEVERAGED_ETF_MAPPING_CSV.values()) + \
    list(TICKERS.keys())+\
    ["IGRO.AX","IBAL.AX" ,"IXI.AX","^GSPC","UPRO",
    "AAPL","INTC","WYNN","URTH","SWRD.L",
    "^RUT","DOGE-USD","BTC-USD","GC=F","VAS.AX","^NDX","^KMARSP","^SPKS"]))