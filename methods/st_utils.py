import pandas as pd
import numpy as np
import streamlit as st
import datetime

import classes.definition as dfn
from proj_consts.consts import STOCKS

def tickers_selector():
    symbols_table = dfn.stock_symbols_tabler()
    uniq_cats = symbols_table["Category"].unique()
    selected = st.selectbox("Category", uniq_cats, key="category")

    category_table = symbols_table.query("Category == @selected")
    event = st.dataframe(category_table[["Symbol","SubCategory"]],
                        use_container_width=True,
                        hide_index=True,
                        on_select="rerun",
                        selection_mode="multi-row")

    selected_tickers = category_table.iloc[event.selection.rows]
    return selected_tickers["Symbol"].to_list()

def choices_section(portfolio = False):
    with st.sidebar:
        night_day(st.session_state)
        if portfolio:
            durations = st.number_input("Investment Duration (Years)", value=10, min_value=1, max_value=40, step=1)
            durations = [durations]
        else:
            durations = st.text_input("Investment Durations (Years)", '10')#'3,5,10,15'
            durations = [float(i) for i in list(durations.split(",")) ]    
        st.date_input(
            "Select raw dates range",
            (datetime.date(1940, 1, 1), datetime.datetime.today()),
            datetime.date(1940, 1, 1),
            datetime.datetime.today(),
            format="DD.MM.YYYY",
            key="raw_dates_range"
        )
        start = st.session_state["raw_dates_range"][0].strftime('%Y-%m-%d')
        end = st.session_state["raw_dates_range"][1].strftime('%Y-%m-%d')
        
        if portfolio:
            symbols = []
        else:
            symbols_selected = st.multiselect(
                label="Symbols",
                options=STOCKS,
                key="selected_symbols",
                max_selections=len(STOCKS),
                default=STOCKS[0:2]
            )
            # symbols_selected = st.session_state["selected_symbols"]

            symbols_manual = st.text_input("Manual Symbols", "^GSPC, ^NDX")
            symbols_manual = list(symbols_manual.split(",")) 
            symbols_manual = symbols_manual if symbols_manual!=[""] else []
            symbols_table = []#tickers_selector()
    
            symbols = list(set(symbols_selected + symbols_manual + symbols_table))
        
        selected_tool = ["yfinance","ta_indices","more_indices"] if dfn.TA_INDICES else ["yfinance"]
        lst_wthrwl = "0"
    ui_choices = {"fin_tools":selected_tool,"lst_wthrwl":lst_wthrwl,
                "symbols":symbols,"durations":durations,"start":start,"end":end}
    return ui_choices
    
def table_filter(tot_transactions, date_col = "withdrawal_date"):
    # plt_table = tot_transactions[tot_transactions["Symbol"
    #                         ].isin(st.session_state["stock"])]
    plt_table = tot_transactions
    plt_table = plt_table[plt_table["Investment Duration"
                            ]==st.session_state["duration"]]
    # date_ranger = lambda df, dates: df[(df[date_col] > dates[0].strftime('%Y-%m-%d')
    #                                     ) & (df[date_col] < dates[1].strftime('%Y-%m-%d'))]
    # revenue_table = date_ranger(plt_table,st.session_state["dates_range"])
    # adj_dates = list(st.session_state["dates_range"])
    # adj_dates[1] = adj_dates[1]+datetime.timedelta(days=365*(st.session_state["duration"]))
    # price_table = date_ranger(plt_table,adj_dates)
    price_table = plt_table
    revenue_table = plt_table
    return revenue_table, price_table

def selections(tot_transactions):
    row_1 = st.columns(2)
    uniq_durations = tot_transactions["Investment Duration"].unique()
    with row_1[1]:
        st.selectbox("Duration",
                     uniq_durations,
                     key="duration")
    with row_1[0]:
        checkbox_normalize = st.checkbox("Normalize Y",True)
    return checkbox_normalize

def night_day(ms):
    """ Simplistic option which sometimes work...
    if st.toggle("Dark Mode", value=True) is False:
          st._config.set_option(f'theme.base', "light")
    else:
          st._config.set_option(f'theme.base', "dark")
    if st.button("Refresh"):
          st.rerun()
    """
    if "themes" not in ms: 
        ms.themes = {"current_theme": "light",
                        "refreshed": True,
                        
                        "light": {"theme.base": "dark",
                                #   "theme.backgroundColor": "black",
                                #   "theme.primaryColor": "#c98bdb",
                                #   "theme.secondaryBackgroundColor": "#5591f5",
                                #   "theme.textColor": "white",
                                #   "theme.textColor": "white",
                                "button_face": "🌜"},

                        "dark":  {"theme.base": "light",
                                #   "theme.backgroundColor": "white",
                                #   "theme.primaryColor": "#5591f5",
                                #   "theme.secondaryBackgroundColor": "#82E1D7",
                                #   "theme.textColor": "#0a1464",
                                "button_face": "🌞"},
                        }
    

    def ChangeTheme():
        previous_theme = ms.themes["current_theme"]
        tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
        for vkey, vval in tdict.items(): 
            if vkey.startswith("theme"): st._config.set_option(vkey, vval)

        ms.themes["refreshed"] = False
        if previous_theme == "dark": ms.themes["current_theme"] = "light"
        elif previous_theme == "light": ms.themes["current_theme"] = "dark"


    btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
    st.button(btn_face, on_click=ChangeTheme)

    if ms.themes["refreshed"] == False:
        ms.themes["refreshed"] = True
        st.rerun()