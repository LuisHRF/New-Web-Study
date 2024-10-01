import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from collections import Counter


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

def kpi_summary(df): # Calculate key performance indicators (KPI) for each variation (Control or Test)

    kpi_summary = df.groupby('Variation').agg(
    avg_logons_6_month=('logons_6_month', 'mean'),
    avg_calls_6_month=('calls_6_month', 'mean'),
    avg_balance=('balance', 'mean'),
    total_clients=('client_id', 'nunique')
    ).reset_index()

    return kpi_summary

def avg_time_per_step(df): # Calculate te aberage time spend in each step

    df['date_time'] = pd.to_datetime(df['date_time'])
    
    df_sorted = df.sort_values(by=['visit_id', 'date_time'])
    
    df_sorted['time_spent'] = df_sorted.groupby(['visit_id'])['date_time'].diff()

    process_step_summary = df_sorted.groupby(['Variation', 'process_step']).agg(
        avg_time_spent=('time_spent', lambda x: x.mean().total_seconds() if pd.notnull(x.mean()) else 0)
    ).reset_index()

    pivot_table = process_step_summary.pivot(index='process_step', columns='Variation', values='avg_time_spent')

    return pivot_table


def conversion_rate(df): # Calculate the conversion rate for each step 

    users_completed_by_variation = df.groupby(['process_step', 'Variation'])['client_id'].nunique().reset_index(name='users_completed')

    total_users_by_variation = df.groupby('Variation')['client_id'].nunique().reset_index(name='total_users')

    conversion_rate_by_step = pd.merge(users_completed_by_variation, total_users_by_variation, on='Variation')

    conversion_rate_by_step['conversion_rate'] = (conversion_rate_by_step['users_completed'] / conversion_rate_by_step['total_users']) * 100

    pivot_table = conversion_rate_by_step.pivot(index='process_step', columns='Variation', values='conversion_rate')

    return pivot_table
    
def average_balance_by_age_group(df): # Calculate the average balance for each age group
    bins = [18, 30, 40, 50, 60, 70, 100]
    labels = ['18-30', '30-40', '40-50', '50-60', '60-70', '70+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    balance_by_age_group = df.groupby(['age_group', 'Variation'])['balance'].mean().reset_index()

    pivot_table = balance_by_age_group.pivot(index='age_group', columns='Variation', values='balance')

    return pivot_table

def analyze_error_rate(df):

    users_completed_by_step = df.groupby(['process_step', 'Variation'])['client_id'].nunique().reset_index(name='users_completed')
    process_order = ['start', 'step_1', 'step_2', 'step_3', 'confirm']
    users_completed_by_step['process_step'] = pd.Categorical(users_completed_by_step['process_step'], categories=process_order, ordered=True)
    users_completed_by_step = users_completed_by_step.sort_values(['Variation', 'process_step'])
    users_completed_by_step['prev_step_users'] = users_completed_by_step.groupby('Variation')['users_completed'].shift(1)
    users_completed_by_step['error_rate'] = ((users_completed_by_step['prev_step_users'] - users_completed_by_step['users_completed']) / users_completed_by_step['prev_step_users']) * 100
    users_completed_by_step['error_rate'] = users_completed_by_step['error_rate'].fillna(0)

    print("\n=== Error Rate Analysis ===")
    for index, row in users_completed_by_step.iterrows():
        if row['error_rate'] > 10:
            print(f"High user loss at '{row['process_step']}' for {row['Variation']} (Error Rate: {row['error_rate']:.2f}%)")
    
    
    plt.figure(figsize=(12, 6))
    
    bar_width = 0.35
    index = range(len(users_completed_by_step['process_step'].unique()))
    
    steps = users_completed_by_step['process_step'].unique()
    control_data = users_completed_by_step[users_completed_by_step['Variation'] == 'Control']['error_rate']
    test_data = users_completed_by_step[users_completed_by_step['Variation'] == 'Test']['error_rate']
    
    plt.bar(index, control_data, width=bar_width, color='red', alpha=0.6, label='Control')
    plt.bar([i + bar_width for i in index], test_data, width=bar_width, color='blue', alpha=0.6, label='Test')
    
    plt.xlabel('Process Steps')
    plt.ylabel('Error Rate (%)')
    plt.title('Error Rate per Process Step by Variation')
    plt.axhline(10, color='gray', linestyle='--', linewidth=0.7, label='Significant Loss Threshold (10%)')
    plt.xticks([r + bar_width / 2 for r in index], steps)
    plt.legend()
    plt.grid(axis='y')
    
    plt.show()
    
    return users_completed_by_step


# Discarded functions

def create_click_path(df): 
    age_bins = [18, 30, 40, 50, 60, 70, 100]
    age_labels = ['18-30', '30-40', '40-50', '50-60', '60-70', '70+']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)

    step_order = {'start': 1, 'step_1': 2, 'step_2': 3, 'step_3': 4, 'confirm': 5}
    df['step_order'] = df['process_step'].map(step_order)

    # Create df
    path_data = []

    # Init a loop each age group and variation
    for age_group in age_labels:
        for variation in ['Control', 'Test']:
            filtered_df = df[(df['age_group'] == age_group) & (df['Variation'] == variation)]
            
            click_sequences = filtered_df.sort_values(by=['visit_id', 'step_order']).groupby('visit_id')['process_step'].apply(lambda x: ' -> '.join(x)).tolist()
            
            path_counts = Counter(click_sequences)
            
            for path, count in path_counts.items():
                path_data.append({
                    'age_group': age_group,
                    'variation': variation,
                    'click_path': path,
                    'count': count
                })
    
    return pd.DataFrame(path_data)
 

def chart_bar_cp_per_age_group(df):
    step_columns = ['start_percentage', 'step_1_percentage', 'step_2_percentage', 'step_3_percentage', 'confirm_percentage']
    step_display_labels = ['Start', 'Step 1', 'Step 2', 'Step 3', 'Confirm']

    age_groups = df['age_group'].unique()

    for age_group in age_groups:
        subset = df[df['age_group'] == age_group]
        
        plt.figure(figsize=(10, 6))
        
        control_data = subset[subset['variation'] == 'Control'][step_columns].iloc[0] if not subset[subset['variation'] == 'Control'].empty else [0] * len(step_columns)
        test_data = subset[subset['variation'] == 'Test'][step_columns].iloc[0] if not subset[subset['variation'] == 'Test'].empty else [0] * len(step_columns)

        bar_width = 0.35
        index = range(len(step_display_labels))

        plt.bar(index, control_data, width=bar_width, label='Control', color='lightblue', alpha=0.7)
        plt.bar(index, test_data, width=bar_width, label='Test', color='lightgreen', alpha=0.7, bottom=control_data)

        plt.xlabel('Process Steps')
        plt.ylabel('Percentage of Users Reaching Each Step (%)')
        plt.title(f'Percentage of Users Reaching Each Step - Age Group: {age_group}')
        plt.xticks(index, step_display_labels)
        plt.legend(title='Variation')
        plt.grid(axis='y')

        plt.show()
