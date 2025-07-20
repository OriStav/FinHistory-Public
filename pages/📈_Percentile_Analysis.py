"""
Portfolio Analysis Page
Analyzes portfolio performance with custom ticker weights

{
  "TQQQ": 230,
  "TA35.TA": 222,
  "^NDX": 81,
  "EVTL": 1075,
  "NKE": 1075,
  "TSLA": 230,
  "NICE.TA": 807,
  "FLHK": 729,
  "EWH": 729,
  "VGS.AX": 726,
  "^RUT": 230,
  "ADM": 230,
  "UPRO": 41,
  "GIS": 230,
  "INTC": 230,
  "EQIX": 230,
  "OOO.AX": 206,
  "OXY": 207,
  "CVX": 207,
  "ASX.AX": 206,
  "UFO": 202,
  "REMX": 202,
  "3X Leveraged TA-35": 192,
  "IYK": 163,
  "TM": 163,
  "^NSEI": 121,
  "BITX": 39
}"""
import streamlit as st
import pandas as pd
import numpy as np
import json
from main import main
from methods.charts_design import make_pretty
from methods.st_utils import choices_section
from proj_consts.consts import COL_CONFIG

st.set_page_config(layout="wide")

# Title
st.title("% Analysis")
st.subheader("Relative Performance Analysis")

# Text input for portfolio dictionary
portfolio_input = st.text_area(
    "Enter Portfolio Dictionary (JSON format):",
    value='{"IBIT": 365, "TA35.TA": 365, "ESTATE15.TA": 365}',
    height=100,
    help="Enter tickers and their durations (days) as a JSON dictionary"
)

# Parse portfolio input
try:
    portfolio_dict = json.loads(portfolio_input)
    REPLACE_TICKERS = {"IBIT":"BTC-USD", "BITX":"2X Leveraged BTC","UPRO":"3X Leveraged S&P"}
    # Replace tickers in the portfolio_dict with their mapped values
    portfolio_dict = {REPLACE_TICKERS.get(k, k): v/365 for k, v in portfolio_dict.items()}

    if not isinstance(portfolio_dict, dict):
        st.error("Input must be a valid dictionary")
        st.stop()
    
    # Validate tickers
    tickers = list(portfolio_dict.keys())
    durations = list(portfolio_dict.values())
    
except json.JSONDecodeError:
    st.error("Invalid JSON format. Please check your input.")
    st.stop()
except Exception as e:
    st.error(f"Error parsing portfolio: {str(e)}")
    st.stop()

# Get user choices from sidebar
ui_choices = choices_section(portfolio = True)
# Override symbols with portfolio tickers
round_stks = pd.DataFrame({"symbol": tickers, "dur_years": durations})

# Analyze each ticker
st.subheader("Portfolio Analysis Results")

sym_dur_rnk, latest, tot_transactions = main(ui_choices, invested_bool=True, round_stks=round_stks)

latest["duration_round"] = latest["duration_round"]*365
latest["average_actual_duration"] = latest["average_actual_duration"]*365
latest["std_actual_duration"] = latest["std_actual_duration"]*365

# Find symbols that are in ui_choices but not in sym_dur_rnk
missing_symbols = set(ui_choices["symbols"]) - set(sym_dur_rnk["Symbol"].unique()) if not sym_dur_rnk.empty else set(ui_choices["symbols"])
if missing_symbols:
    st.warning(f"**Warning:** The following symbols were not found in the analysis results: {', '.join(missing_symbols)}")
    # st.dataframe(sym_dur_rnk_tst[["Symbol","tool_age"]],hide_index=True,use_container_width=False)

# Calculate statistics for each ticker
if not latest.empty:
    # Group by symbol and calculate statistics
    # Apply styling similar to app.py
    styled_df = latest.set_index(['Symbol','duration_round']).style.pipe(make_pretty)
    
    # Display the table
    st.dataframe(
        styled_df,
        use_container_width=True,
        column_config=COL_CONFIG
    )
    
    # Show detailed data
    with st.expander("Detailed Investment Data"):
        st.write("**Raw Investment Data:**")
        st.dataframe(tot_transactions, use_container_width=True)
        
        st.write("**Ranking Data:**")
        st.dataframe(sym_dur_rnk, use_container_width=True)
        
        st.write("**Latest Data:**")
        st.dataframe(latest, use_container_width=True)

else:
    st.warning("No data available for the selected tickers and parameters. Please check your input and try different parameters.")

st.write("---")
st.write("**Data Doesn't Lie... But it Doesn't Tell the Whole Story**")
st.write("**OS made**, 2024") 