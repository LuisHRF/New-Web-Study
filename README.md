# 🚀 **Testing A/B: Analysis of New Website Impact for Vanguard** 

![](https://github.com/LuisHRF/New-Web-Study/blob/main/dashboard_gif/power_bi_dashboard.gif)


## 💻 Team Members 

| Nombre             | LinkedIn                                  |
|----------------------------------|-------------------------------------------|
| Luis H. Rodríguez Fuentes	 |   [LinkedIn](https://www.linkedin.com/in/luis-h-rodr%C3%ADguez-fuentes/)    |
| Haridian Lugo Morays        |   [LinkedIn](https://www.linkedin.com/in/haridian-morays-242023329/)   |


## 📋 Table of Contents 
- Project Overview
- Data Sources 
- Project Structure
- Methodology
- Major obstacle
- Conclusions
- Tools and Technologies Used


## ✨ Context and Project Overview

This project is part of the Data Analyst and Data Science bootcamp at Ironhack (Spain).

The goal of this project is to evaluate the impact of a new web interface on user behavior and engagement compared to the traditional version. We used a controlled A/B testing experiment from March 15th, 2017, to June 20th, 2017, and focused on key metrics such as conversion rate, error rate, and customer drop-offs per process step.

## 📑 Data Sources 

- [Client Profiles](https://github.com/data-bootcamp-v4/lessons/blob/main/5_6_eda_inf_stats_tableau/project/files_for_project/df_final_demo.txt)

- [Digital Footprints (df_final_web_data) pt_1](https://github.com/data-bootcamp-v4/lessons/blob/main/5_6_eda_inf_stats_tableau/project/files_for_project/df_final_web_data_pt_1.txt)

- [Digital Footprints (df_final_web_data) pt_2](https://github.com/data-bootcamp-v4/lessons/blob/main/5_6_eda_inf_stats_tableau/project/files_for_project/df_final_web_data_pt_2.txt)

- [Experiment Roster](https://github.com/data-bootcamp-v4/lessons/blob/main/5_6_eda_inf_stats_tableau/project/files_for_project/df_final_experiment_clients.txt)

## 📁 Repository Structure
New-Web-Study/                                     
├── charts_png/                                                                    
│   ├── age_group_distribution_for_variation.png                                                    
│   ├── avg_time_per_step.png                                                                                
│   ├── calls_n_logons.png                                 
│   ├── conversion_n_dropout_rate.png                                        
│   └── performance_by_age_group.png
├── data/                                                                                        
│   ├── power_bi_tables/                                        
│   │   ├── age_distribution.csv                                                                     
│   │   ├── avg_time_per_step.csv                                                                                             
│   │   ├── completion_rate_by_age_group.csv                                                                                    
│   │   ├── error_rate.csv                                                                                                                                              
│   ├── raw/                                                                                                                       
│   │   ├── df_final_clients_data.csv                                                                                                
│   │   ├── df_final_demo_cleanead.csv                                                                                                   
│   │   └── df_web_total_data.csv                                                                     
│   ├── df_final_clients_data.csv                                                            
│   ├── df_final_demo_cleanead.csv                                                                   
│   └── df_web_data_total.csv                                                                     
├── notebooks/                                                                       
│   ├── draft/                                                                        
│   │   ├── Vanguard_check_nan.ipynb                                                        
│   │   ├── main_draft.ipynb                                                 
│   ├── Vanguard_ml_lighgbm.ipynb                                              
│   ├── functions.py                                                                                
│   ├── main.ipynb                                                             
│   └── powerbi_functions.py                                         
├── config.yaml   
├── power_bi_dashboard_testing_ab.pbix                                                                                                                     
├── requirements.txt                                                      
└── README.md     

## 📚 Methodology

### 1. Data Preparation and Cleaning

The customer data has been collected from internal resources during the A/B testing phase. This includes detailed records of customer interactions, service usage, and engagement metrics relevant to our analysis.

After that, we developed a general function to be able to observe the main characteristics of each data frame (see: rows, columns, data type, nulls...) and in this way determine whether a data frame should be subjected to a cleaning process or not.

```python
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
```

Afterwards, the objetive was:

- Merged demographic data (df_final_demo_cleanead.csv) with experimental client data (experiment_non_nan.csv)
- Combined web navigation data (df_web_data_total.csv) to build a unified dataset for analysis

### 2. EDA (Exploratory Data Analysis)

The target was conducted univariate and bivariate analyses to explore relationships between demographic attributes and conversion rates; and analyzed key metrics such as average time spent at each step, the number of logins, and the effect of account balance on completion rates.

Using libraries such as Pandas, NumPy, and Seaborn, we developed a series of functions and scripts to analyze user interactions.

### 3. Hypothesis Testing through DataViz

We used Matplotlib and Seaborn for graphical visualizations, presenting insights through line plots and bar charts to effectively illustrate average times and completion rates.

Data visualization plays a key role in deriving clear insights from the experiment and understanding customer interactions. Throughout the analysis, several key charts were created to provide a detailed view of the performance of both control and test groups.

#### 3.1. Key Metrics

- **Average Time Spent**: We calculated the average time users spend at each step of the process, segmented by age group and variation.

    ```python
    def avg_time_per_step(df): # Calculate te aberage time spend in each step

        df['date_time'] = pd.to_datetime(df['date_time'])
    
        df_sorted = df.sort_values(by=['visit_id', 'date_time'])
    
        df_sorted['time_spent'] = df_sorted.groupby(['visit_id'])['date_time'].diff()

        process_step_summary = df_sorted.groupby(['Variation', 'process_step']).agg(
            avg_time_spent=('time_spent', lambda x: x.mean().total_seconds() if pd.notnull(x.mean()) else 0)
        ).reset_index()

        pivot_table = process_step_summary.pivot(index='process_step', columns='Variation', values='avg_time_spent')

        return pivot_table
    ```

- **Completion Rates**: We analyzed how variations in the interface affect completion rates across different age groups.

    ```python
    completion_rate_final = pd.merge(last_step_completion, total_clients_by_age, on=['age_group', 'Variation'])
    completion_rate_final['completion_rate'] = (completion_rate_final['client_id'] / completion_rate_final['total_users']) * 100
    ```

- **Performance by Age Group**: We categorized users into age groups and computed metrics for each process step to identify trends in user behavior.

    ```python
    df_sorted = df_age_performance.sort_values(by=['visit_id', 'date_time'])

    df_sorted['time_spent'] = df_sorted.groupby(['visit_id'])['date_time'].diff()

    avg_time_by_age_group = df_sorted.groupby(['age_group', 'Variation', 'process_step']).agg(
        avg_time_spent=('time_spent', lambda x: x.mean().total_seconds() if pd.notnull(x.mean()) else 0)
        ).reset_index()

    pivot_time_age = avg_time_by_age_group.pivot(index=['age_group', 'process_step'], columns='Variation', values='avg_time_spent')

    pivot_time_age
    ```
    
- **Error rate**: A function that calculated the percentage of error (drop in users) in each step compared to the previous one between the Control and Test groups (to see the code: notebooks/functions.py)

### 4. Machine Learning Model

> [!NOTE]
> In a real work exercise, it would not have been necessary to run this model to determine which of the nulls belonged to Test and Control. In a real context, this could be a data flaw, but since this is a learning project, we decided to use a predictive Machine Learning model to be able to apply it and work with more data.

The project includes a machine learning component to predict the variation ('Test' or 'Control') for clients in cases where this information is missing. The model is built using a LightGBM Classifier with hyperparameter tuning via GridSearchCV. Below is a summary of the modeling steps:

#### Modeling Process

> 4.1 Data Preparation

- Merged demographic data, web interaction data, and experiment client data to create a complete dataset (```final_data_clean```).
- Handled missing values and encoded categorical variables ('gender' and 'process_step') using ```LabelEncoder```.
- Split data into training and testing sets with an 80-20 ratio.

> 4.2 Model Selection and Hyperparameter Tuning:

- Chose LightGBM as the base classifier and defined a grid of hyperparameters (```num_leaves```, ```learning_rate```, ```n_estimators```, and ```feature_fraction```).
- Used GridSearchCV to find the best combination of parameters.
- Achieved an accuracy of **78.6%** on the test set with the best parameters.

> 4.3 Feature Importance Analysis:

- Calculated feature importance to identify which variables had the most influence on the prediction.
- Top features included ```balance```, ```age```, and ```seniority_per_months```.

> 4.5 Handling Missing Variations:

- Predicted missing values for the 'Variation' column using the best-trained LightGBM model.
- Imputed missing variation values and verified the consistency of the final dataset.

#### Key results

- **Best Model Parameters:**
```python
{
    'feature_fraction': 1.0,
    'learning_rate': 0.1,
    'n_estimators': 200,
    'num_leaves': 100
}
```

- **Model Accuracy**: 78.6% after hyperparameter tuning.

- Feature Importance:

```balance```, ```age```, ```seniority_per_months```, and ```calls_6_month``` were among the most important features for classification.

### 4. Dasboard using Power BI

Finally, we created a series of tables in ```main.ipynb``` to be able to create a dashboard in Power Bi (you can see how it works and the structure in the gif shared at the beginning of this ```README```.

In the dashboard we go into detail about: Global Error, Number of users by Age Group, Completion Rate by User Group (Control vs. Test), Time spend per step (Control vs. Test), Clients by age and balance (Control vs. Test), Clients difference between Control and Test and Client by logons and calls.

## 🔍 Major obstacle

First, the biggest hurdle was deciding what to do with the null values ​​within ```Variation```, as it was the most important variable because it determines whether or not the user entered the new website. Since it was a learning exercise, we decided to apply a predictive model to determine which users belonged to Control and which to Test.

Thus, we decided to apply PCA for dimensionality reduction and used Random Forest to predict variation based on customer attributes. But the accuracy of the model left a lot to be desired, as it did not exceed **51%**.

This is why, finally, we opted for a Machine Learning model based on decision trees that achieved **78%** accuracy.

Secondly, we had a big problem when it came to coordinating the work. Since it was such a large project, the workflows varied a lot and we had to maintain great coordination to avoid errors in the uploads to Git.

## 📊 Conclusions (in terms of objectives)

The analysis provides a comprehensive view of how the new digital interface affects customer interactions. The results highlight areas for improvement and strengths that we will now highlight.

- **Age group distribution for control and test groups**: This analysis examines the proportion of customers within different age groups for both control and test variations, providing insights into demographic distribution.
  ![age_group_distribution_for_variation](https://github.com/LuisHRF/New-Web-Study/blob/luis_branch/charts_png/age_group_distribution_for_variation.png?raw=true)
  
- **Average time per step for control and test**: This plot illustrates the average time users spent on each process step, comparing the control group to the test group, offering insights into the user journey's efficiency.
![avg_time_per_step](https://github.com/LuisHRF/New-Web-Study/blob/luis_branch/charts_png/avg_time_per_step.png?raw=true)

- **Comparison of calls and logons by variation**: This compares the number of calls and logins by users in the control group versus the test group, providing insights into engagement levels.
![calls_n_logons](https://github.com/LuisHRF/New-Web-Study/blob/luis_branch/charts_png/calls_n_logons.png?raw=true)

- **Conversion rate and dropout rate per step for control and test**: This visualization focuses on the conversion rates and dropout rates at each step of the process for both groups, highlighting where users tend to drop off.
![conversion_n_dropout_rate](https://github.com/LuisHRF/New-Web-Study/blob/luis_branch/charts_png/conversion_n_dropout_rate.png?raw=true)

- **Average time and completion rate by age group (control vs test)**: A combined analysis that includes:
  - A line plot showing the **average time spent per step** by different age groups in both control and test groups.
  - A bar plot representing the **completion rates** for each age group in the control and test groups, highlighting differences in behavior and interaction between age demographics.
![performance_by_age_group](https://github.com/LuisHRF/New-Web-Study/blob/luis_branch/charts_png/performance_by_age_group.png?raw=true)

## 🛠️ Tools and Technologies Used

- **Programming Language**: Python
- **Libraries**: Pandas, NumPy, Scipy, Collections
- **Visualization**: Matplotlib, Seaborn, Power BI
- **Machile Learning**: LightGBM, PCA (discard)
- **Jupyter Notebook**: For documentation and interactive analysis.
