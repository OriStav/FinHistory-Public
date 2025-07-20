"""
if invested_bool = True -> 
runnable through uni_mock only...
since round_stks is from FinancialStory
"""
#%%
from methods.explainer import latest_rnk

from classes.investor import invest,invested
from methods import explainer
from classes.definition import defs
# from classes import visuals 

def main(ui_choices:dict = None, invested_bool = False, round_stks = None):
    tot_transactions,_,_,sym_dur_rnk= main_util(ui_choices,invested_bool, round_stks)
    sym_dur_rnk = sym_dur_rnk.reset_index()
    selected_cols = [x for x in sym_dur_rnk.columns.values if "rank" not in x]
    selected_cols.append("rank_overall")
    sym_dur_rnk = sym_dur_rnk[selected_cols]
    latest,_ = latest_rnk(tot_transactions)
    return sym_dur_rnk, latest, tot_transactions

def main_util(ui_choices:dict = None, invested_bool = False, round_stks = None):
    dfn = defs(ui_choices)
    if invested_bool:
        stocks_df,tot_transactions = invested(dfn, round_stks)
    else:
        stocks_df,tot_transactions = invest(dfn)
    sym_dur_grp=explainer.agg_sym_dur(tot_transactions)
    sym_dur_rnk=explainer.rnk(sym_dur_grp)
    tot_transactions = tot_transactions.reset_index(drop=True)
    return tot_transactions,stocks_df,sym_dur_grp,sym_dur_rnk

if __name__=="__main__":
    import os
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    tot_transactions,stocks_df,sym_dur_grp,sym_dur_rnk = main_util(invested_bool=False)