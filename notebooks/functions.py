import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn


def data_summary(df): # Function for before all and check the raw dataframes

    # Check rows and colums
    shape = df.shape
    print("Number of columns ->", shape[1])
    print("Number of rows ->", shape[0])

    # Check duplicates rows
    check_duplicates = df.duplicated().sum()
    print("Number of duplicates ->", check_duplicates)

    # Create a dataframe with original df type information
    df_summary = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes,
        'Values Count': df.notnull().sum(),
        'Null Values': df.isnull().sum(),
        'Unique Values': df.nunique()
    })

    return df_summary

def rename_demo_columns(df): #Rename the columns from df_final_demo

    columns_names = {
        "clnt_tenure_yr": "seniority_per_years",
        "clnt_tenure_mnth": "seniority_per_months",
        "clnt_age": "age",
        "gendr": "gender",
        "num_accts": "number_of_accounts",
        "bal": "balance",
        "calls_6_mnth": "calls_6_month",
        "logons_6_mnth": "logons_6_month"
    }

    df_renamed_columns = df.rename(columns=columns_names).copy()

    return df_renamed_columns

# KPI/Metrics functions

def kpi_summary(df):

    kpi_summary = df.groupby('Variation').agg(
    avg_logons_6_month=('logons_6_month', 'mean'),
    avg_calls_6_month=('calls_6_month', 'mean'),
    avg_balance=('balance', 'mean'),
    total_clients=('client_id', 'nunique')
    ).reset_index()

    return kpi_summary

def avg_time_per_step(df):

    df['date_time'] = pd.to_datetime(df['date_time'])
    
    df_sorted = df.sort_values(by=['visit_id', 'date_time'])
    
    df_sorted['time_spent'] = df_sorted.groupby(['visit_id'])['date_time'].diff()

    process_step_summary = df_sorted.groupby(['Variation', 'process_step']).agg(
        avg_time_spent=('time_spent', lambda x: x.mean().total_seconds() if pd.notnull(x.mean()) else 0)
    ).reset_index()

    pivot_table = process_step_summary.pivot(index='process_step', columns='Variation', values='avg_time_spent')

    return pivot_table


def conversion_rate(df):

    # Calcular el número de usuarios que completan cada step agrupado por Variation (Test o Control)
    users_completed_by_variation = df.groupby(['process_step', 'Variation'])['client_id'].nunique().reset_index(name='users_completed')

    total_users_by_variation = df.groupby('Variation')['client_id'].nunique().reset_index(name='total_users')

    conversion_rate_by_step = pd.merge(users_completed_by_variation, total_users_by_variation, on='Variation')

    conversion_rate_by_step['conversion_rate'] = (conversion_rate_by_step['users_completed'] / conversion_rate_by_step['total_users']) * 100

    pivot_table = conversion_rate_by_step.pivot(index='process_step', columns='Variation', values='conversion_rate')

    return pivot_table
    
def average_balance_by_age_group(df):
    bins = [18, 30, 40, 50, 60, 70, 100]
    labels = ['18-30', '30-40', '40-50', '50-60', '60-70', '70+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    balance_by_age_group = df.groupby(['age_group', 'Variation'])['balance'].mean().reset_index()

    pivot_table = balance_by_age_group.pivot(index='age_group', columns='Variation', values='balance')

    return pivot_table

