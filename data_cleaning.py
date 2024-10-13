import pandas as pd
import numpy as np

# Load the scraped data
data = pd.read_csv('scraped_job_vacancies_data.csv')

# Step 1: Drop rows where 'Job Type' is missing
data_cleaned = data.dropna(subset=['Job Type']).copy()

# Step 2: Drop rows where 'Salary' is 'Undisclosed'
data_cleaned = data_cleaned[data_cleaned['Salary'].str.lower() != 'undisclosed']

# Step 3: Drop the 'Job URL' column (not needed for prediction)
data_cleaned = data_cleaned.drop(columns=['Job URL'])

# Step 4: Function to process the salary values
def process_salary(salary_str):
    salary_str = salary_str.replace('RM', '').replace(',', '').strip()
    
    # Handle 'K' for thousands (e.g., '5K' -> '5000')
    if 'K' in salary_str:
        salary_str = salary_str.replace('K', '000')
    
    if '-' in salary_str:  # Salary range (e.g., "2500 - 2800")
        salary_min, salary_max = salary_str.split('-')
        return (float(salary_min.strip()) + float(salary_max.strip())) / 2  # Take the average
    else:  # Single salary value (e.g., "8000")
        return float(salary_str)

# Step 5: Apply the salary processing function
data_cleaned['Salary'] = data_cleaned['Salary'].apply(process_salary)

# Step 6: Save the cleaned data without one-hot encoding
data_cleaned.to_csv('cleaned_job_vacancies_data.csv', index=False)

print("Data cleaned and saved to 'cleaned_job_vacancies_data.csv'")
