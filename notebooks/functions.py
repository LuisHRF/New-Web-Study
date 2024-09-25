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

def calculate_avg_time_per_step(df): # Function to calculate the average time in seconds per step
    # Sort values
    df_sorted = df.sort_values(by=['visit_id', 'process_step', 'date_time'], ascending=[True, True, False])
    df_sorted = df_sorted.drop_duplicates(subset=['visit_id', 'process_step'], keep='first').reset_index(drop=True)

    # Divide by variation
    df_control = df_sorted[df_sorted['Variation']=='Control'].reset_index(drop=True)
    df_test = df_sorted[df_sorted['Variation']=='Test'].reset_index(drop=True)

    def step_times(df):
        # Dictionary by step
        steps = ['start', 'step_1', 'step_2', 'step_3', 'confirm']
        step_df = {step: df[df['process_step'] == step][['visit_id', 'date_time']].rename(columns={'date_time': f'date_time_{step}'}) for step in steps}

        # Merge dataframes by visit_id
        df = step_df['start']
        for step in steps[1:]:
            df = pd.merge(df, step_df[step], on='visit_id', how='inner')

        time_spent = {
            'step 1': (df['date_time_step_1'] - df['date_time_start']).mean().total_seconds(),
            'step 2': (df['date_time_step_2'] - df['date_time_step_1']).mean().total_seconds(),
            'step 3': (df['date_time_step_3'] - df['date_time_step_2']).mean().total_seconds(),
            'confirm': (df['date_time_confirm'] - df['date_time_step_3']).mean().total_seconds()
        }

        return time_spent
    
    time_per_step_control = step_times(df_control)
    time_per_step_test = step_times(df_test)

    # Create DF
    time_spent_df = pd.DataFrame({
        'Control': time_per_step_control,
        'Test': time_per_step_test
    })

    return time_spent_df

def calculate_conversion_n_dropout(df):
    # Sort values
    df_sorted = df.sort_values(by=['visit_id', 'process_step', 'date_time'], ascending=[True, True, False])

    # Divide by variation
    df_control = df_sorted[df_sorted['Variation']=='Control'].reset_index(drop=True)
    df_test = df_sorted[df_sorted['Variation']=='Test'].reset_index(drop=True)

    def calculate_rates(df):
        step_counts = df.groupby(['process_step']).size()

        #Calculate conversion
        conversion_rate = (step_counts.cumsum() / step_counts.sum()) * 100


        # Calculate dropout
        dropout_rate = 1 - (conversion_rate / 100)

        return conversion_rate, dropout_rate
    
    # Calculate each variation
    conversion_rate_control, dropout_rate_control = calculate_rates(df_control)
    conversion_rate_test, dropout_rate_test = calculate_rates(df_test)

    conversion_dropout_df = pd.DataFrame({
        'control_conversion_rate': conversion_rate_control,
        'control_dropout_rate': dropout_rate_control,
        'test_conversion_rate': conversion_rate_test,
        'test_dropout_rate': dropout_rate_test
    })

    return conversion_dropout_df

