import pandas as pd
from typing import Optional
import time
from methods.miner import mine

def trade(dfn_import, source: Optional[str]="yfinance"):
    global dfn
    dfn = dfn_import
    stocks_df = pd.DataFrame()
    logger = dfn.logger
    stocks_df = mine(dfn, source)
    if len(stocks_df):
        transactions = stocks_loop(stocks_df)
    else:
        Exception("____no data____")
    return stocks_df,transactions
    
def stocks_loop(stocks_df):
    start = time.perf_counter()
    stocks_grps = stocks_df.groupby("Symbol")
    transactions = pd.DataFrame()
    for stock in stocks_grps:
        stock_data = stock[1].dropna().reset_index()
        lg = f"{stock[0]} ,len: {len(stock[1])}, after nans dropped: {len(stock_data)}"
        dfn.logger.debug(lg)  
        if len(stock_data):
            new_transactions = calc_deltas(stock_data)
            new_transactions["Symbol"] = stock[0]
            transactions = pd.concat([transactions,
                                          new_transactions])
        else:
            Exception(f"____no data for {stock[0]}____")
    transactions = post_calcs(transactions)
    end = time.perf_counter()
    dfn.logger.info(f"time to run stocks_loop {end - start:.2f} seconds")
    dfn.logger.info(f"tolearnce diff days max: {round(transactions['days_deviation'].max()*365,0)}")
    return transactions

def post_calcs(dif_table):
    dif_table["investment_duration"] = ((dif_table["withdrawal_date"] -
                               dif_table["investment_date"]).dt.days)/365
    dif_table["days_deviation"] = dif_table["investment_duration"] - dfn.invst_dur
    dif_table["delta"] = dif_table["withdrawal_close"]-dif_table["investment_close"]
    #delta_in_perc_per_year:
    dif_table["yearly_profit_percentage"] = 100*((dif_table["withdrawal_close"
                           ]/dif_table["investment_close"])**(1/dfn.invst_dur)-1)
    return dif_table

def drop_xtrm_qntl(dif:pd.Series):
    # also possible to use zscore ->  np.abs(stats.zscore(dif))
    q_low = dif.quantile(0.01)
    q_hi  = dif.quantile(0.99)
    df_filtered = dif[(dif< q_hi) & (dif > q_low)]
    if len(df_filtered)<len(dif)/100:#for cases there are no outliers
        dfn.logger.info(f"no outliers: mean_dif = {dif.mean()}, len dif = {len(dif)}, len df_filtered= {len(df_filtered)}")
        df_filtered = dif
    return df_filtered.dropna()

def calc_deltas(stock):
    """
    # tst : 100*((15400/9500)^(1/5)-1)
    """
    dif_table = pd.DataFrame()
    mean_dif = drop_xtrm_qntl(stock["Date"].diff().dt.days).mean()
    rows_mean_skip = int(round(dfn.invst_dur*365/mean_dif,0))
        
    stock["Date"] = stock["Date"].sort_values()
    dif_table["investment_date"] = stock["Date"].shift(rows_mean_skip)
    dif_table["investment_close"] = stock["Close"].shift(rows_mean_skip)
    dif_table["withdrawal_date"] = stock["Date"].shift(-rows_mean_skip)
    dif_table["withdrawal_close"] = stock["Close"].shift(-rows_mean_skip)
    dif_table = dif_table[dif_table["investment_date"].notnull()] 
    dif_table = dif_table[dif_table["withdrawal_date"].notnull()]

    return dif_table

def rename_same_name_columns(withdrawal,investment):
    withdrawal=withdrawal.rename({"Date": "Withdrawal Date",
                                  "Close": "Withdrawal Close"},axis='columns')
    investment=investment.rename({"Date": "Investment Date",
                                  "Close": "Investment Close"},axis='columns')
    return withdrawal,investment