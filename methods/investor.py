import pandas as pd
from methods.stocker import trade

def invest(dfn):
    tot_transactions,stocks_df = pd.DataFrame(),pd.DataFrame()
    for tool in ["yfinance"]:#preparation to add options in app
        for dur in dfn.durations:
            stocks_df,tot_transactions = stock_durrer(dur,tool,dfn,
                                                      stocks_df,tot_transactions)
    return stocks_df,tot_transactions

def invested(dfn):
    tot_transactions,stocks_df = pd.DataFrame(),pd.DataFrame()
    by_dur = dfn.invested.groupby("dur_years")["symbol"
                                               ].apply(lambda x:
                                                       ",".join(x).split(",")
                                                       ).reset_index()
    for index, row in by_dur.iterrows():
        dfn.symbols = row["symbol"]
        stocks_df,tot_transactions = stock_durrer(row["dur_years"],"yfinance",stocks_df,tot_transactions)                            
    return stocks_df,tot_transactions

def stock_durrer(invst_dur,fin_tool,dfn,stocks_df,tot_transactions):
    dfn.invst_dur = invst_dur
    stk_df,trnscs = trade(dfn,fin_tool)# fin_tool
    tot_transactions = pd.concat([tot_transactions, trnscs])
    stocks_df=pd.concat([stocks_df, stk_df])
    return stocks_df,tot_transactions