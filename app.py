"""
streamlit run app.py
https://market.tase.co.il/he/market_data/indices?dType=1&oId=03
""" 
import streamlit as st

from main import main
from methods.charts_design import tables_presenter,lines_presenter,\
                                    dist_presenter,error_bander
from methods.st_utils import choices_section

st.set_page_config(layout="wide")

st.markdown("""
<div style="text-align: center;">
    <h1>Historical Performance of Stocks & Indices</h1>
    <h3>Comparative Statistical Analysis</h3>
</div>
""", unsafe_allow_html=True)

with st.expander("Explanations"):
    st.write("This is a statistical tool to compare historical\
              performance of stocks & indices from yahoo finance")
    st.write("It is built so that the highest level of analysis is \
             shown at the top of the page and below is the dive in")
    st.write("The Historical rank and Timing rank are meant to be used as KPIs.")
    st.write("Usage suggestion:")
    st.write("First choose parameters on the sidebar")
    st.write("Compare groups of tickers by sectors you want to invest in,\
             then compare the chosen tickers combined to find the best")
    st.write("*No growth correction for timing rank is made, its importance\
             lower due to the comparative nature of the analysis")
    st.write("*Dividends are not included in profit calculation")
# user choices
ui_choices = choices_section()
#data prep

sym_dur_rnk, latest, tot_transactions = main(ui_choices)
uc_range = ui_choices
#present data
selected_rows = tables_presenter(sym_dur_rnk, latest)
tot_transactions.rename(columns = {"yearly_profit_percentage":"Average Annual Revenue [%]"},inplace=True)
tot_transactions.columns = [i.replace("_"," ").title() for i in tot_transactions.columns]

def error_bander_row(tot_transactions):
    bands_row = st.columns([1,2])
    selected = bands_row[0].selectbox(
        "Revenue Bands Stock",
        ui_choices["symbols"],
        key="stock"
    )
    values = bands_row[1].slider("Select a range of durations", 1, 100, (1, 11))
    # st.write(selected_rows)
    # if not selected_rows.empty:
    #     selected = selected_rows.reset_index()["Symbol"][0]
    # else:
    #     selected = ui_choices["symbols"][0]
    uc_range["symbols"] = [selected]

    uc_range["durations"] = range(values[0],values[1])
    sym_dur_rnk_range, _, _ = main(uc_range)

    error_band = error_bander(sym_dur_rnk_range.sort_values("investment_duration"),name = uc_range["symbols"][0],
                            outer_bound=True, inner_bound=True)
    return error_band

dist_presenter(tot_transactions)
lines_presenter(tot_transactions)
error_band = error_bander_row(tot_transactions)
st.plotly_chart(error_band)


present_tot_transactions = tot_transactions.copy()
# Format date columns to d m y format
for col in present_tot_transactions.columns:
    if present_tot_transactions[col].dtype == 'datetime64[ns]':
        present_tot_transactions[col] = present_tot_transactions[col].dt.strftime('%d/%m/%Y')

st.write(present_tot_transactions)
st.write("Data Doesn't Lie... But it Doesn't Tell the Whole Story")
st.write("**OS made**, 2024")