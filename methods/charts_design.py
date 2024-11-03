import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale
import streamlit as st
import datetime
import altair as alt
import plotly.express as px
import plotly.figure_factory as ff

from methods.st_utils import selections,table_filter

def multi_hister(tot_transactions):
    plt_tbl = tot_transactions.pivot(\
                        index="investment_date",
                            values='yearly_profit_percentage',
                            columns=['Symdur'])
    multi_hist = alt.Chart(plt_tbl).transform_fold(
        plt_tbl.columns.to_list(),
        as_=['Experiment', 'Measurement']
    ).mark_bar(
        opacity=0.5,
        binSpacing=0
    ).encode(
        alt.X('Measurement:Q').bin(maxbins=100),
        alt.Y('count()').stack(None),
        alt.Color('Experiment:N')
    ).interactive()

    st.altair_chart(multi_hist)


def alt_violin(tot_transactions,para = "yearly_profit_percentage",by = "Symdur"):
    violin = alt.Chart(tot_transactions).transform_density(
        para,
        as_=[para, 'density'],
        # extent=[5, 50],
        groupby=[by]
    ).mark_area(orient='horizontal').encode(
        alt.X('density:Q')
            .stack('center')
            .impute(None)
            .title(None)
            .axis(labels=False, values=[0], grid=False, ticks=True),
        alt.Y(f'{para}:Q'),
        alt.Color(f'{by}:N'),
        alt.Column(f'{by}:N')
            .spacing(0)
            .header(titleOrient='bottom', labelOrient='bottom', labelPadding=0)
    ).configure_view(
        stroke=None
    ).interactive()

    st.altair_chart(violin)

def dist_presenter(tot_transactions):
    tot_transactions["investment_duration"] = tot_transactions["investment_duration"
                                                               ].round(0).astype(int).astype(str)
    string_concater = lambda x: x["Symbol"]+"_"+x["investment_duration"]
    tot_transactions["Symdur"] = tot_transactions.apply(string_concater,axis=1)
    symdurs = tot_transactions["Symdur"].unique().tolist()
    with st.expander("Distributions"):
        fig = px.histogram(tot_transactions, x="yearly_profit_percentage", 
                color="Symdur", marginal="box") # or violin, rug
        st.plotly_chart(fig)

def lines_presenter(tot_transactions):
    tot_transactions["investment_duration"] = tot_transactions["investment_duration"
                                                           ].round(0).astype(int)
    selections(tot_transactions)
    revenue_table, price_table = table_filter(tot_transactions)
    row_1 = st.columns(2)
    with row_1[0]:
        alt_line_plot(revenue_table)
    with row_1[1]:
        header_row = st.columns(3)
        if header_row[2].toggle("Normalize Y",True):
            price_table = normalizer(price_table)
        
        header_row[1].subheader("Price timeline")
        alt_line_plot(price_table,header=None,y_col="withdrawal_close")

def tables_presenter(sym_dur_rnk, latest):

    sym_dur_rnk, latest, sym_dur = tables_designer(sym_dur_rnk, latest)
    row_1 = st.columns(5)
    # row_1[2].text("   sorting will make a mess    ")
    space1 = pd.DataFrame({"":[""]*len(sym_dur_rnk)},index=sym_dur_rnk.index)
    space2 = pd.DataFrame({" ":[""]*len(sym_dur_rnk)},index=sym_dur_rnk.index)
    sym_dur_rnk = pd.concat([sym_dur_rnk,space1,sym_dur,space2,latest],axis=1)

    iv_column = st.column_config.TextColumn(label="Duration 💬",
                                            help="Investment *Mean* Duration in Years")
    or_column = st.column_config.TextColumn(label="History Rank 💬",
                                            help=f"Combining {', '.join(sym_dur.columns)}")
    tr_column = st.column_config.TextColumn(label="Timing Rank 💬",
                                            help="By current percentile")
    st.dataframe(sym_dur_rnk.style.pipe(make_pretty),height=None,
                column_config={"Investment Duration": iv_column,
                                "Rank Overall":or_column,
                                "Timing Rank":tr_column},hide_index=True)

def alt_line_plot(plt_table, header = "Yearly profit %",x_col='withdrawal_date',
                  y_col='yearly_profit_percentage',
                  color_col='Symbol'):
    chart = alt.Chart(plt_table).mark_line(interpolate="basis").encode(
        x=x_col,
        y=y_col,
        color=color_col
    ).interactive()
    if header:
        header_row = st.columns(3)
        header_row[1].subheader(header)
    st.altair_chart(chart, use_container_width=True)

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

def normalizer(df, val="withdrawal_close", cat="Symbol"):
    scaler = lambda x: 100*x/x.max()
    df.reset_index(inplace=True)
    scaled = df.groupby(cat)[val].apply(scaler).rename(val).reset_index(drop=True)
    # scaled = pd.Series(100*df.groupby(cat)[val].apply(minmax_scale)[0]).rename(val)
    df.drop(columns=val, inplace=True)
    scaled_df = pd.concat([df,scaled],axis=1)
    return scaled_df
