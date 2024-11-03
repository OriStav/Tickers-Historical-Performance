#%%
from methods.explainer import latest_rnk
from methods.investor import invest,invested
from methods import explainer
from methods.definition import defs

def main(ui_choices:dict = None):
    tot_transactions,_,_,sym_dur_rnk= main_util(ui_choices)
    sym_dur_rnk = sym_dur_rnk.reset_index()
    selected_cols = [x for x in sym_dur_rnk.columns.values if "rank" not in x]
    selected_cols.append("rank_overall")
    sym_dur_rnk = sym_dur_rnk[selected_cols]
    latest,_ = latest_rnk(tot_transactions)
    return sym_dur_rnk, latest, tot_transactions

def main_util(ui_choices:dict = None):
    #for testing mostly (no need for Streamlit input)
    dfn = defs(ui_choices)
    stocks_df,tot_transactions = invest(dfn)
    sym_dur_grp=explainer.agg_sym_dur(tot_transactions)
    sym_dur_rnk=explainer.rnk(sym_dur_grp)
    tot_transactions = tot_transactions.reset_index(drop=True)
    return tot_transactions,stocks_df,sym_dur_grp,sym_dur_rnk

if __name__=="__main__":
    tot_transactions,stocks_df,sym_dur_grp,sym_dur_rnk = main_util()