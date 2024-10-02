# 🚀 **Analysis of Digital Experiments at Vanguard** 

This is a data analysis project within the Ironhack Data Analysis Bootcamp.

[Link to the presentation]( )


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


## ✨ Project Overview

This project aims to analyze customer experience trends during a digital experiment at Vanguard, focusing on the impact of a new interface on user interactions. The goal is to derive insights that can enhance customer engagement strategies. Below is a description of the methods used for data collection, analysis, and visualization.

## 📑 Data Sources 

- [Client Profiles](https://github.com/data-bootcamp-v4/lessons/blob/main/5_6_eda_inf_stats_tableau/project/files_for_project/df_final_demo.txt)

- [Digital Footprints (df_final_web_data) pt_1](https://github.com/data-bootcamp-v4/lessons/blob/main/5_6_eda_inf_stats_tableau/project/files_for_project/df_final_web_data_pt_1.txt)

- [Digital Footprints (df_final_web_data) pt_2](https://github.com/data-bootcamp-v4/lessons/blob/main/5_6_eda_inf_stats_tableau/project/files_for_project/df_final_web_data_pt_2.txt)

- [Experiment Roster](https://github.com/data-bootcamp-v4/lessons/blob/main/5_6_eda_inf_stats_tableau/project/files_for_project/df_final_experiment_clients.txt)

## 📁 Project Structure
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

### 1. Data Collection

The customer data has been collected from internal resources during the A/B testing phase. This includes detailed records of customer interactions, service usage, and engagement metrics relevant to our analysis.

### 2. Data Cleaning

We addressed data quality issues stemming from inconsistencies in the original datasets, such as incomplete interaction logs and formatting errors. Column names were standardized for improved readability, and data types were adjusted to ensure accuracy and compatibility with our analysis. NaN values were completed with a predictive algorithm.

### 3. Data Analysis

Using libraries such as Pandas, NumPy, and Seaborn, we developed a series of functions and scripts to analyze user interactions. Here are some examples of functions created:

- **Average Time Spent**: We calculated the average time users spend at each step of the process, segmented by age group and variation.

    ```python
    avg_time_by_age_group = df_sorted.groupby(['age_group', 'Variation', 'process_step']).agg(
        avg_time_spent=('time_spent', lambda x: x.mean().total_seconds() if pd.notnull(x.mean()) else 0)
    ).reset_index()
    ```

- **Completion Rates**: We analyzed how variations in the interface affect completion rates across different age groups.

    ```python
    completion_rate_final = pd.merge(last_step_completion, total_clients_by_age, on=['age_group', 'Variation'])
    completion_rate_final['completion_rate'] = (completion_rate_final['client_id'] / completion_rate_final['total_users']) * 100
    ```

- **Performance by Age Group**: We categorized users into age groups and computed metrics for each process step to identify trends in user behavior.

    ```python
    df_age_performance['age_group'] = pd.cut(df_age_performance['age'], bins=age_bins, labels=age_labels, right=False)
    ```

### 4. Data Visualization

We used Matplotlib and Seaborn for graphical visualizations, presenting insights through line plots and bar charts to effectively illustrate average times and completion rates.

Data visualization plays a key role in deriving clear insights from the experiment and understanding customer interactions. Throughout the analysis, several key charts were created to provide a detailed view of the performance of both control and test groups.


## 🔍 Major obstacle


## 📊 Conclusions

The analysis provides a comprehensive view of how the new digital interface affects customer interactions. Findings highlight areas for improvement and offer insights into the demographics most affected by the changes.

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
- **Libraries**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Power BI
- **Jupyter Notebook**: For documentation and interactive analysis.
