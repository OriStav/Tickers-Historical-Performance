import pandas as pd
import numpy as np
import streamlit as st
import datetime

import methods.definition as dfn

def tickers_selector():
    symbols_table = dfn.tickers
    uniq_cats = symbols_table["Category"].unique()
    selected = st.selectbox("Category", uniq_cats, key="category")

    category_table = symbols_table.query("Category == @selected")
    event = st.dataframe(category_table[["Symbol"]],
                        use_container_width=True,
                        hide_index=True,
                        on_select="rerun",
                        selection_mode="multi-row")

    selected_tickers = category_table.iloc[event.selection.rows]
    return selected_tickers["Symbol"].to_list()

def choices_section():
    with st.sidebar:
        night_day(st.session_state)
        durations = st.text_input("Investment Durations (Years)", '3,10')#'3,5,10,15'
        durations = [int(i) for i in list(durations.split(",")) ]    
        lst_wthrwl = st.text_input("Investment Last Withdrawal (Years Ago)", '0')
        lst_wthrwl = int(lst_wthrwl)
        
        symbols_options = ["IGRO.AX","IBAL.AX" ,"IXI.AX","^GSPC",
                           "AAPL","INTC","WYNN","URTH","SWRD.L","^RUT","DOGE-USD","BTC-USD","GC=F","VAS.AX"]
        symbols_selected = st.multiselect(
            label="Symbols",
            options=symbols_options,
            key="selected_symbols",
            max_selections=len(symbols_options),
            default=["URTH"]
        )
        symbols_manual = st.text_input("Manual Symbols", '^GSPC')
        symbols_manual = list(symbols_manual.split(",")) 
        
        symbols_table = tickers_selector()
        
        symbols = list(set(symbols_selected + symbols_manual + symbols_table))
        
    ui_choices = {"lst_wthrwl":lst_wthrwl,
                "symbols":symbols,"durations":durations}
    return ui_choices
    
def table_filter(tot_transactions, date_col = "withdrawal_date"):
    plt_table = tot_transactions[tot_transactions["Symbol"
                            ].isin(st.session_state["stock"])]
    plt_table = plt_table[plt_table["investment_duration"
                            ]==st.session_state["duration"]]
    date_ranger = lambda df, dates: df[(df[date_col] > dates[0].strftime('%Y-%m-%d')
                                        ) & (df[date_col] < dates[1].strftime('%Y-%m-%d'))]
    revenue_table = date_ranger(plt_table,st.session_state["dates_range"])
    adj_dates = list(st.session_state["dates_range"])
    adj_dates[1] = adj_dates[1]+datetime.timedelta(days=365*(st.session_state["duration"]))
    price_table = date_ranger(plt_table,adj_dates)
    return revenue_table, price_table

def selections(tot_transactions):
    uniq_stocks = tot_transactions["Symbol"].unique()
    row_1 = st.columns(5)
    with row_1[1]:
        selected = st.multiselect(
            "Stocks",
            uniq_stocks,
            uniq_stocks,
            key="stock"
        )

    first_year = 2021
    jan_1 = tot_transactions["withdrawal_date"].min()
    dec_31 = tot_transactions["withdrawal_date"].max()
    
    with row_1[2]:
        d = st.date_input(
            "Select dates range",
            (datetime.date(first_year, 1, 1), dec_31),
            jan_1,
            dec_31,
            format="DD.MM.YYYY",
            key="dates_range"
        )
    
    uniq_durations = tot_transactions["investment_duration"].unique()
    with row_1[3]:
        st.selectbox("Duration",
                     uniq_durations,
                     key="duration")

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
                                "button_face": "🌜"},

                        "dark":  {"theme.base": "light",
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