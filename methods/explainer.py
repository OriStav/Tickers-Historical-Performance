import pandas as pd
import numpy as np

def rnker(df):
    rnk=100*df.rank(pct=True,numeric_only=True,na_option='bottom')
    return rnk

def latest_rnk(tot_trans):
    tot_transactions = tot_trans.copy()
    tot_transactions["duration_round"] = tot_transactions["investment_duration"].round(0)#.astype(int)#.dt.days
    average_actual_duration = tot_transactions.groupby(["Symbol","duration_round"])["investment_duration"].mean(
                                                            ).rename("average_actual_duration")
    std_actual_duration = tot_transactions.groupby(["Symbol","duration_round"])["investment_duration"].std(
                                                            ).rename("std_actual_duration")
    grp_dur = pd.concat([average_actual_duration,std_actual_duration],axis=1)


    grp_rnk = tot_transactions.groupby(["Symbol","duration_round"])["yearly_profit_percentage"
                                                       ].apply(rnker
                                                       ).rename("current_percentile"
                                                ).reset_index(level=[0,1],drop=True)
    tot_transactions=pd.concat([tot_transactions,grp_rnk],axis=1)
    max_date = tot_transactions.groupby(["Symbol","duration_round"])["withdrawal_date"
                                                       ].max()
                                                
    latest_no_vals = pd.concat([grp_dur,max_date],axis=1).reset_index()
                                                           
    latest = latest_no_vals.merge(tot_transactions[["withdrawal_date","Symbol",
                                                "duration_round","current_percentile","yearly_profit_percentage"]],
                                                how="inner",on=["withdrawal_date",
                                                            "Symbol","duration_round"])
    return latest, tot_transactions

def latest_rnk_og(tot_transactions):
    grp_rnk = tot_transactions.groupby("Symbol")["yearly_profit_percentage"
                                                       ].apply(rnker
                                                       ).rename("current_percentile"
                                                ).reset_index(level=0, drop=True)
    
    tot_transactions=pd.concat([tot_transactions,grp_rnk],axis=1)
    
    max_date = tot_transactions.groupby("Symbol")["investment_date"
                                                       ].max(
                                                ).reset_index(level=0, drop=True)
    
    latest=tot_transactions.merge(max_date,how="inner"
                                  ).drop_duplicates("Symbol")[["Symbol","current_percentile"]]
    latest["timing_rank"] = 100 - latest["current_percentile"]
    return latest

def agg_sym_dur(tot_transactions:pd.DataFrame)->pd.DataFrame:
    tot_transactions=tot_transactions.copy()
    tot_transactions["investment_duration"]=tot_transactions["investment_duration"].round(0)

    sym_dur_grp=tot_transactions.groupby(["Symbol","investment_duration"])['yearly_profit_percentage'].describe()
    sym_dur_grp=add_tool_age(tot_transactions,sym_dur_grp)
    sym_dur_grp=sym_dur_grp.reset_index(level='investment_duration')#move investment_duration from index to columns
    return sym_dur_grp

def rnk(sym_dur_grp:pd.DataFrame)->pd.DataFrame:
    rnk=100*sym_dur_grp.rank(pct=True,numeric_only=True,na_option='bottom')
    
    rnk['std']=100-rnk['std']
    rnk["overall"]=rnk.mean(axis=1)
    
    c_dict=dict(zip(rnk.columns,"rank_"+ rnk.columns))
    rnk=rnk.rename(columns=c_dict)
    
    sym_dur_rnk=pd.concat([sym_dur_grp,rnk],axis=1)
    return sym_dur_rnk

def add_tool_age(tot_transactions,sym_dur_grp):
    d_dur=tot_transactions.groupby("Symbol").apply(data_dur)
    sym_dur_grp=sym_dur_grp.join(d_dur.rename("tool_age"))
    return sym_dur_grp
def data_dur(df):
    return (max(df["withdrawal_date"])-min(df["investment_date"])).days/365
