import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
accepted_df = pd.read_csv('accepted_2007_to_2018Q4.csv')

#I am dropping the following columns because they all have over 1,000,000 nan values
#In a dataset of 2.2 million records this is a very singificant portion of blank values
#I also dropped URL because I don't see how that adds value
drop_columns = ['member_id','desc','mths_since_last_delinq','mths_since_last_record','next_pymnt_d','mths_since_last_major_derog','annual_inc_joint','dti_joint','verification_status_joint','il_util','mths_since_recent_bc_dlq','mths_since_recent_revol_delinq','revol_bal_joint','sec_app_fico_range_low','sec_app_fico_range_high','sec_app_earliest_cr_line','sec_app_inq_last_6mths','sec_app_mort_acc','sec_app_open_acc','sec_app_revol_util','sec_app_open_act_il','sec_app_num_rev_accts','sec_app_chargeoff_within_12_mths','sec_app_collections_12_mths_ex_med','sec_app_mths_since_last_major_derog','hardship_type','hardship_reason','hardship_status','deferral_term','hardship_amount','hardship_start_date','hardship_end_date','payment_plan_start_date','hardship_length','hardship_dpd','hardship_loan_status','orig_projected_additional_accrued_interest','hardship_payoff_balance_amount','hardship_last_payment_amount','debt_settlement_flag_date','settlement_status','settlement_date','settlement_amount','settlement_percentage','settlement_term','url']
accepted_df.drop(drop_columns, axis=1, inplace=True)
accepted_df.dropna(inplace=True)
#After dropping all rows with missing data, we are left with just over 1 million records and 106 columns

#NOTE - For visualizations, please see the notebook in the same repository 

#Based on my own estimations, I grouped the 100 columns into the following groups
loan_data = ['id','loan_amnt','funded_amnt','funded_amnt_inv','term','int_rate','installment','grade','sub_grade','purpose']
customer_data = ['id','emp_title','emp_length','home_ownership','annual_inc','verification_status','issue_d']
credit_history = ['id','loan_status','pymnt_plan','purpose','title','zip_code','addr_state',
'dti','delinq_2yrs','earliest_cr_line','fico_range_low','fico_range_high','inq_last_6mths','open_acc','pub_rec','revol_bal','revol_util','total_acc']
payment_details = ['id','out_prncp','out_prncp_inv','total_pymnt','total_pymnt_inv','total_rec_prncp','total_rec_int','total_rec_late_fee','recoveries','collection_recovery_fee','last_pymnt_d','last_pymnt_amnt','last_credit_pull_d','last_fico_range_high','last_fico_range_low','collections_12_mths_ex_med']
#I have a lot less confidence in this group as I do the others. I don't like that it is so large and I am not sure
#that all of these columns are account details. Many of these abbreviations are unfamiliar to me so there is a lot of 
#guesswork in this group
account_details = ['id','application_type','acc_now_delinq','tot_coll_amt','tot_cur_bal','open_acc_6m','open_act_il','open_il_12m','open_il_24m','mths_since_rcnt_il','total_bal_il','open_rv_12m','open_rv_24m','max_bal_bc','all_util','total_rev_hi_lim','inq_fi','total_cu_tl','inq_last_12m','acc_open_past_24mths','avg_cur_bal','bc_open_to_buy','bc_util','chargeoff_within_12_mths','delinq_amnt','mo_sin_old_il_acct','mo_sin_old_rev_tl_op','mo_sin_rcnt_rev_tl_op','mo_sin_rcnt_tl','mort_acc','mths_since_recent_bc','mths_since_recent_inq','num_accts_ever_120_pd','num_actv_bc_tl','num_actv_rev_tl','num_bc_sats','num_bc_tl','num_il_tl','num_op_rev_tl','num_rev_accts','num_rev_tl_bal_gt_0','num_sats','num_tl_120dpd_2m','num_tl_30dpd','num_tl_90g_dpd_24m','num_tl_op_past_12m','pct_tl_nvr_dlq','percent_bc_gt_75','pub_rec_bankruptcies','tax_liens','tot_hi_cred_lim','total_bal_ex_mort','total_bc_limit','total_il_high_credit_limit','hardship_flag','disbursement_method','debt_settlement_flag']

#Instantiating sqlite DB
sqlite_db = 'lendingclub-db'
con = sqlite3.connect(sqlite_db)

#Storing all CSV contents into sqlite db
#Note that all validation was handled earlier when I filtered out columns with high rates of blank values
#I then dropped all nan rows after so I have confidence in the quality of the data
accepted_df[loan_data].to_sql('loan_data', con, if_exists='replace', index=False)
accepted_df[customer_data].to_sql('customer_data', con, if_exists='replace', index=False)
accepted_df[credit_history].to_sql('credit_history', con, if_exists='replace', index=False)
accepted_df[payment_details].to_sql('payment_details', con, if_exists='replace', index=False)
accepted_df[account_details].to_sql('account_details', con, if_exists='replace', index=False)
#There is limited overhead necessary in creating sqlite tables from dataframes. The column names in the dataframe
#will persist in the table schema

#After persisting, let's test that we can load the data
loan_df = pd.read_sql_query('SELECT * FROM loan_data', con)
customer_df = pd.read_sql_query('SELECT * FROM customer_data', con)
credit_df = pd.read_sql_query('SELECT * FROM credit_history', con)
payment_df = pd.read_sql_query('SELECT * FROM payment_details', con)
account_df = pd.read_sql_query('SELECT * FROM account_details', con)

#Here, we just ensure the shape of the shape returned from the table matches the shape we put in
if loan_df.shape != accepted_df[loan_data].shape:
    print('ERROR, LOAN TABLE MISMATCH')
if customer_df.shape != accepted_df[customer_data].shape:
    print('ERROR, CUSTOMER TABLE MISMATCH')
if credit_df.shape != accepted_df[credit_history].shape:
    print('ERROR, CREDIT TABLE MISMATCH')
if payment_df.shape != accepted_df[payment_details].shape:
    print('ERROR, PAYMENT TABLE MISMATCH')
if account_df.shape != accepted_df[account_details].shape:
    print('ERROR, ACCOUNT TABLE MISMATCH')
