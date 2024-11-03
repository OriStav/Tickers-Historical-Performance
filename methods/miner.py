import pandas as pd
import yfinance as yf
from typing import Optional
import time

def mine(dfn_import,source: Optional[str]="yfinance"):
    global dfn
    dfn = dfn_import

    start = time.perf_counter()
    stocks_df=pd.DataFrame()
    if source=="yfinance":
        stocks_df = yfinance_handling()
    end = time.perf_counter()
    dfn.logger.info(f"\ntime to run Miner {end - start:.2f} seconds")
    return stocks_df

def yfinance_handling():
    stocks_df = yf.download(dfn.symbols)
    stocks_df = yf_multi_stocks_handling(stocks_df)
    return stocks_df


def yf_multi_stocks_handling(stocks_df)->pd.DataFrame:
    a = stocks_df.copy()
    if isinstance(a.columns, pd.MultiIndex):
        ix=a.columns.droplevel(1).str.match("Close")
    else:
        ix=a.columns.str.match("Close")
        
    b=a.loc[:,ix]#keep only Close value columns
    
    if isinstance(a.columns, pd.MultiIndex):
        b.columns=b.columns.droplevel(0)#rename columns to stock symbols
    else:
        b.columns = dfn.symbols

    c=b.melt(value_vars=b.columns,var_name="Symbol", 
                          value_name='Close',ignore_index=False)
    stocks_df=c.reset_index()
    return stocks_df
