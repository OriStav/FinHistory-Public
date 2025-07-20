"""
Portfolio Analysis Page
Analyzes portfolio performance with custom ticker weights
"""
import streamlit as st
import pandas as pd
import numpy as np
import json
from main import main
from methods.charts_design import make_pretty
from methods.st_utils import choices_section
from proj_consts.consts import COL_CONFIG_WEIGHTS

st.set_page_config(layout="wide")

# Title
st.title("Portfolio Analysis")
st.subheader("Custom Portfolio Performance Analysis")

with st.expander("Instructions"):
    st.write("Enter a dictionary of tickers and their weights in the format:")
    st.write('{"BTC-USD": 5, "TA35.TA": 3, "ESTATE15.TA": 2, "BITX": 1, "UPRO": 1,"NFLX": 1}')
    st.write("The system will analyze each ticker and show median and standard deviation statistics.")
    st.write("Select your investment parameters in the sidebar.")

# Portfolio input section
st.subheader("Portfolio Configuration")

# Text input for portfolio dictionary
portfolio_input = st.text_area(
    "Enter Portfolio Dictionary (JSON format):",
    value='{"BTC-USD": 5, "^GSPC": 3, "^NDX": 2, "BITX": 1, "UPRO": 1,"NFLX": 1}',
    height=100,
    help="Enter tickers and their weights as a JSON dictionary"
)

# Parse portfolio input
try:
    portfolio_dict = json.loads(portfolio_input)
    REPLACE_TICKERS = {"IBIT":"BTC-USD", "BITX":"2X Leveraged BTC","UPRO":"3X Leveraged S&P"}
    # Replace tickers in the portfolio_dict with their mapped values
    portfolio_dict = {REPLACE_TICKERS.get(k, k): v for k, v in portfolio_dict.items()}

    if not isinstance(portfolio_dict, dict):
        st.error("Input must be a valid dictionary")
        st.stop()
    
    # Validate tickers
    tickers = list(portfolio_dict.keys())
    weights = list(portfolio_dict.values())
    total_weight = sum(weights)
    
except json.JSONDecodeError:
    st.error("Invalid JSON format. Please check your input.")
    st.stop()
except Exception as e:
    st.error(f"Error parsing portfolio: {str(e)}")
    st.stop()

# Get user choices from sidebar
ui_choices = choices_section(portfolio = True)
durations_save = ui_choices["durations"]
# Override symbols with portfolio tickers
ui_choices["symbols"] = tickers

# Analyze each ticker
st.subheader("Portfolio Analysis Results")

# Get data for all tickers
def duration_mapper(ui_choices, durations_save):
    ui_choices["durations"] = [1]
    sym_dur_rnk_tst, _, _ = main(ui_choices)
    def my_floor(a, precision=0):
        return np.round(a - 0.5 * 10**(-precision), precision)

    ui_choices["durations"] = durations_save
    # Calculate duration years based on tool age and minimum duration
    sym_dur_rnk_tst["dur_years"] = sym_dur_rnk_tst["tool_age"].apply(
        lambda x: min(my_floor(x, 0), ui_choices["durations"][0])
    )

    round_stks = sym_dur_rnk_tst[["Symbol","dur_years"]].rename(columns={"Symbol":"symbol"})
    return round_stks
    
round_stks = duration_mapper(ui_choices, durations_save)

sym_dur_rnk, latest, tot_transactions = main(ui_choices, invested_bool=True, round_stks=round_stks)

# st.write(sym_dur_rnk)

# Find symbols that are in ui_choices but not in sym_dur_rnk
missing_symbols = set(ui_choices["symbols"]) - set(sym_dur_rnk["Symbol"].unique()) if not sym_dur_rnk.empty else set(ui_choices["symbols"])
if missing_symbols:
    st.warning(f"**Warning:** The following symbols were not found in the analysis results: {', '.join(missing_symbols)}")
    # st.dataframe(sym_dur_rnk_tst[["Symbol","tool_age"]],hide_index=True,use_container_width=False)

# Calculate statistics for each ticker
if not tot_transactions.empty:
    # Group by symbol and calculate statistics
    stats_df = tot_transactions.groupby('Symbol').agg({
        'yearly_profit_percentage': ['median', 'std', 'mean', 'min', 'max', 'count']
    }).round(2)
    
    # Flatten column names and ensure it's a DataFrame
    stats_df.columns = ['Median Return [%]', 'Std Dev [%]', 'Mean Return [%]', 
                       'Min Return [%]', 'Max Return [%]', 'Sample Count']
    stats_df = stats_df.reset_index()
    
    # Add weight information
    stats_df['Weight'] = [portfolio_dict.get(symbol, 0) for symbol in stats_df['Symbol']]
    stats_df['Weight %'] = (stats_df['Weight'] / total_weight * 100).round(1)
    
    # Reorder columns
    column_order = ['Symbol', 'Weight', 'Weight %', 'Median Return [%]', 'Std Dev [%]', 
                   'Mean Return [%]', 'Min Return [%]', 'Max Return [%]', 'Sample Count']
    stats_df = stats_df[column_order]
    
    # Calculate portfolio-level statistics
    st.write("**Individual Ticker Statistics:**")
    
    # Apply styling similar to app.py
    styled_df = stats_df.set_index('Symbol').style.pipe(make_pretty)
    
    # Display the table
    st.dataframe(
        styled_df,
        use_container_width=True,
        column_config=COL_CONFIG_WEIGHTS
    )
    
    # Portfolio-level summary
    st.subheader("Portfolio Summary")
    
    # Calculate weighted statistics
    weighted_mean = np.average(stats_df['Mean Return [%]'], weights=stats_df['Weight'])
    weighted_median = np.average(stats_df['Median Return [%]'], weights=stats_df['Weight'])
    
    # Simple portfolio volatility (weighted average of individual volatilities)
    weighted_vol = np.average(stats_df['Std Dev [%]'], weights=stats_df['Weight'])
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Weighted Mean Return", f"{weighted_mean:.2f}%")
    with col2:
        st.metric("Weighted Median Return", f"{weighted_median:.2f}%")
    with col3:
        st.metric("Portfolio Weighted Volatility", f"{weighted_vol:.2f}%")
    with col4:
        weighted_min = np.average(stats_df['Min Return [%]'], weights=stats_df['Weight'])
        st.metric("Weighted Min Return", f"{weighted_min:.2f}%")
    with col5:
        weighted_max = np.average(stats_df['Max Return [%]'], weights=stats_df['Weight'])
        st.metric("Weighted Max Return", f"{weighted_max:.2f}%")
    # Risk-return scatter plot
    st.subheader("Risk-Return Analysis")
    
    # Create scatter plot
    import plotly.express as px
    
    fig = px.scatter(
        stats_df,
        x='Std Dev [%]',
        y='Median Return [%]',
        size='Weight',
        hover_data=['Symbol', 'Weight %', 'Mean Return [%]'],
        title="Risk-Return Profile by Ticker"
    )
    
    fig.update_layout(
        xaxis_title="Risk (Standard Deviation) [%]",
        yaxis_title="Return (Median) [%]",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
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