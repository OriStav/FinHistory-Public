import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# from sklearn.preprocessing import minmax_scale
import streamlit as st
import datetime
import altair as alt
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px

from methods.st_utils import selections,table_filter

def dist_presenter(tot_transactions,col = "Investment Duration", x_col="Average Annual Revenue [%]"):
    tot_transactions[col] = tot_transactions[col].round(0).astype(int).astype(str)
                                                               
    string_concater = lambda x: x["Symbol"]+" "+x[col]+" years investment"
    tot_transactions["Simulation Name"] = tot_transactions.apply(string_concater,axis=1)
    symdurs = tot_transactions["Simulation Name"].unique().tolist()
    with st.expander("Distributions"):
        fig = px.histogram(tot_transactions, x=x_col, 
                color="Simulation Name", marginal="box") # or violin, rug
        st.plotly_chart(fig)


def lines_presenter(tot_transactions,col = "Investment Duration",y_col_name = "Withdrawal Close"):
    tot_transactions[col] = tot_transactions[col].round(0).astype(int)
    checkbox_normalize = selections(tot_transactions)
    revenue_table, price_table = table_filter(tot_transactions)
    row_1 = st.columns(2)
    with row_1[1]:
        plotly_line(revenue_table)
    with row_1[0]:
        # header_row = st.columns(3)
        # checkbox_normalize = header_row[0].checkbox("Normalize Y",True)
        if checkbox_normalize:
            price_table = normalizer(price_table)
        
        # header_row[1].subheader("Price timeline")
        plotly_line(price_table,header="Price timeline",y_col=y_col_name)

def tables_presenter(sym_dur_rnk, latest):

    sym_dur_rnk, latest, sym_dur = tables_designer(sym_dur_rnk, latest)
    row_1 = st.columns(5)
    space1 = pd.DataFrame({"":[""]*len(sym_dur_rnk)},index=sym_dur_rnk.index)
    space2 = pd.DataFrame({" ":[""]*len(sym_dur_rnk)},index=sym_dur_rnk.index)
    sym_dur_rnk = pd.concat([sym_dur_rnk,space1,sym_dur,space2,latest],axis=1)

    iv_column = st.column_config.TextColumn(label="Duration 💬",
                                            help="Investment *Mean* Duration in Years")
    or_column = st.column_config.TextColumn(label="History Rank 💬",
                                            help=f"Combining {', '.join(sym_dur.columns)}")
    tr_column = st.column_config.TextColumn(label="Timing Rank 💬",
                                            help="By current percentile")
    sym_dur_rnk.set_index(["Symbol","Investment Duration"],inplace=True)

    # sel = st.dataframe(sym_dur_rnk.style.pipe(make_pretty),height=None,
    #             column_config={"Rank Overall":or_column,
    #                            "Timing Rank":tr_column},hide_index=False,
    #                            selection_mode="multi-row")
    
    # if "df" not in st.session_state:
    st.session_state.df = sym_dur_rnk
        # st.session_state.data = 0

    event = st.dataframe(
        st.session_state.df.style.pipe(make_pretty),
        column_config={"Rank Overall":or_column,
                               "Timing Rank":tr_column},
        key="data",
        # on_select="rerun",
        # selection_mode="single-row",
    )
    # st.write(st.session_state.data["selection"]["rows"])
    # st.write(sym_dur_rnk.iloc[st.session_state.data["selection"]["rows"]])
    return None#sym_dur_rnk.iloc[st.session_state.data["selection"]["rows"]]

def plotly_line(plt_table, header = "Annualized Revenue [%]",x_col='Withdrawal Date',
                  y_col='Average Annual Revenue [%]',
                  color_col='Symbol'):
    fig = px.line(plt_table, x=x_col, y=y_col, color=color_col, markers=False)
    fig.update_layout(title=header, title_font_size=25)
    # if header:
    #     header_row = st.columns(3)
    #     header_row[1].subheader(header)
    st.plotly_chart(fig)

def tables_designer(sym_dur_rnk, latest):
    latest = latest.rename(columns = {"duration_round":"investment_duration"})
    latest = latest.merge(sym_dur_rnk,on=["investment_duration","Symbol"])
    latest_main_columns = ["current_percentile","yearly_profit_percentage","rank_overall"]

    sym_dur_rnk["investment_duration"] = sym_dur_rnk["investment_duration"].astype(int)
    sym_dur_rnk["count"] = sym_dur_rnk["count"].astype(int)
    sym_dur_rnk["timing_rank"] = 100*latest["current_percentile"].rank(pct=True, ascending=False)
    sym_dur_rnk["combined_rank"] = sym_dur_rnk[["timing_rank","rank_overall"]].mean(axis=1)
    col_view = ["Symbol","investment_duration","rank_overall","timing_rank","combined_rank"]
    col_details = [i for i in sym_dur_rnk.columns if i not in ["Symbol","investment_duration"]]

    latest = vis_prep(latest[latest_main_columns].sort_values("rank_overall",
                                            ascending=False).drop(columns='rank_overall'))
    sym_dur = vis_prep(sym_dur_rnk[col_details].sort_values("rank_overall",
                                            ascending=False).drop(columns=["rank_overall","timing_rank","combined_rank"]))
    sym_dur_rnk = vis_prep(sym_dur_rnk[col_view].sort_values("rank_overall",ascending=False))   
        
    return sym_dur_rnk, latest, sym_dur

def vis_prep(df: pd.DataFrame):
    df.index = df.index + 1

    for field in df:
        if df[field].dtypes == np.dtype('datetime64[ns]'):
            #TODO: caveats, returning-a-view-versus-a-copy
            df[field]=df[field].dt.strftime('%d-%b-%Y')
        # df["entrance_date"] = df["entrance_date"].apply(lambda x: x.strftime('%d/%m/%Y')) 
    df.columns = [i.replace("_"," ").title() for i in df.columns]

    return df

def std_pretty(styler):
    cm_r = sns.light_palette("green", as_cmap=True, reverse=True)
    styler.background_gradient(cmap=cm_r,subset = "Std")
    return styler

def make_pretty(styler):
    cm = sns.light_palette("green", as_cmap=True)
    styler.format(precision=1, thousands=",", decimal=".")
    # styler.format({"count": "{:,.0f}".format,"DurationDelta": "{:,.0f}".format})
    styler.background_gradient(cmap=cm)
    return styler

def normalizer(df, val="Withdrawal Close", cat="Symbol"):
    scaler = lambda x: 100*x/x.max()
    df.reset_index(inplace=True)
    scaled = df.groupby(cat)[val].apply(scaler).rename(val).reset_index(drop=True)
    # scaled = pd.Series(100*df.groupby(cat)[val].apply(minmax_scale)[0]).rename(val)
    df.drop(columns=val, inplace=True)
    scaled_df = pd.concat([df,scaled],axis=1)
    return scaled_df

def error_bander(df, med="50%", horiz="investment_duration", 
                  upper_name="max", lower_name="min",
                  mid_upper_name="75%", mid_lower_name="25%",
                  outer_bound = True, inner_bound = True, name = ""):
    """
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/wind_speed_laurel_nebraska.csv')
    error_bander(tot_transactions.sort_values("investment_date") ,
                med="investment_close",horiz="investment_date")
    upper, lower = 1.5*df[med], 0.5*df[med]
    """
    upper, lower = df[upper_name], df[lower_name]
    mid_upper, mid_lower = df[mid_upper_name], df[mid_lower_name]
    
    fig = go.Figure([
        go.Scatter(
            name='Measurement',
            x=df[horiz],
            y=df[med],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        )])
    
    if outer_bound:  
        fig.add_trace(go.Scatter(
            name='Upper Bound',
            x=df[horiz],
            y=upper,
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            name='Lower Bound',
            x=df[horiz],
            y=lower,
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        ))

    if inner_bound: 
        fig.add_trace(go.Scatter(
            name='MidUpper Bound',
            x=df[horiz],
            y=mid_upper,
            mode='lines',
            marker=dict(color="red"),
            line=dict(width=0),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            name='MidLower Bound',
            x=df[horiz],
            y=mid_lower,
            marker=dict(color="red"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(30, 100, 30, 0.3)',
            fill='tonexty',
            showlegend=False
        ))

    fig.update_layout(
        yaxis=dict(title=dict(text='Annualized Revenue [%]')),
        xaxis=dict(title=dict(text='Investment duration [years]')),
        title=dict(text=f'{name} - Annualized revenue [50%, 25%-75%, min-max] Vs Investment duration'),
        hovermode="x"
    )
    # fig.show()
    return fig
    
