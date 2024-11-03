"""
streamlit run app.py
""" 
import streamlit as st

from main import main
from methods.charts_design import tables_presenter,lines_presenter,dist_presenter
from methods.st_utils import choices_section

st.set_page_config(layout="wide")

title_row = st.columns([1,3,1])
title_row[1].title("Historical Performance of Stocks & Indices")
title_row = st.columns([1,1,1])
title_row[1].subheader("Comparative Statistical Analysis")

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
#present data
tables_presenter(sym_dur_rnk, latest)
dist_presenter(tot_transactions)
lines_presenter(tot_transactions)

st.write("Data Doesn't Lie... But it Doesn't Tell the Whole Story")
st.write("**OS made**, 2024")