import pandas as pd
import numpy as np


def age_distribution(df):
    age_bins = [18, 30, 40, 50, 60, 70, 100]
    age_labels = ['18-30', '30-40', '40-50', '50-60', '60-70', '70+']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)
    
    unique_clients_count = df.groupby(['age_group', 'Variation'])['client_id'].nunique().reset_index()
    unique_clients_count.rename(columns={'client_id': 'unique_clients_count'}, inplace=True)
    
    return unique_clients_count

def avg_time_per_step_table(df):
    df['date_time'] = pd.to_datetime(df['date_time'])
    df_sorted = df.sort_values(by=['visit_id', 'date_time'])
    df_sorted['time_spent'] = df_sorted.groupby(['visit_id'])['date_time'].diff()
    
    process_step_summary = df_sorted.groupby(['Variation', 'process_step']).agg(
        avg_time_spent=('time_spent', lambda x: x.mean().total_seconds() if pd.notnull(x.mean()) else 0)
    ).reset_index()
    
    return process_step_summary

def completion_rate_by_age_group(df):
    bins = [18, 30, 40, 50, 60, 70, 100]
    labels = ['18-30', '30-40', '40-50', '50-60', '60-70', '70+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    
    users_by_group = df.groupby(['age_group', 'Variation'])['client_id'].nunique().reset_index(name='users_count')
    users_completed_by_group = df[df['process_step'] == 'confirm'].groupby(['age_group', 'Variation'])['client_id'].nunique().reset_index(name='users_completed')
    
    completion_rate = pd.merge(users_by_group, users_completed_by_group, on=['age_group', 'Variation'], how='left')
    completion_rate['completion_rate'] = (completion_rate['users_completed'] / completion_rate['users_count']) * 100
    
    return completion_rate


def error_rate(df):
    users_completed_by_step = df.groupby(['process_step', 'Variation'])['client_id'].nunique().reset_index(name='users_completed')

    process_order = ['start', 'step_1', 'step_2', 'step_3', 'confirm']

    users_completed_by_step['process_step'] = pd.Categorical(users_completed_by_step['process_step'], categories=process_order, ordered=True)

    users_completed_by_step = users_completed_by_step.sort_values(['Variation', 'process_step'])
    users_completed_by_step['prev_step_users'] = users_completed_by_step.groupby('Variation')['users_completed'].shift(1)
    
    users_completed_by_step['error_rate'] = ((users_completed_by_step['prev_step_users'] - users_completed_by_step['users_completed']) / users_completed_by_step['prev_step_users']) * 100
    users_completed_by_step['error_rate'] = users_completed_by_step['error_rate'].fillna(0)

    return users_completed_by_step

def calls_logons(df):
    clients_table = df[['client_id', 'calls_6_month', 'logons_6_month', 'Variation']].drop_duplicates(subset=['client_id'])

    return clients_table

