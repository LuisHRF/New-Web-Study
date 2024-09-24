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
