---

# **Salary Prediction for Job Listings**

## **1. Project Overview**

In this project, I developed a salary prediction model using machine learning techniques. The data for this project was scraped from a job portal (Hiredly) and used to build a regression model that predicts the salary based on the **Job Title**, **Location**, and **Job Type**. The models were trained and compared using different machine learning algorithms, such as **Random Forest** and **XGBoost**.

---

## **2. Objective**

The main objective of this project was to predict the salary of job listings based on categorical features:
- **Job Title**
- **Location**
- **Job Type**

Additionally, I aimed to compare the performance of different machine learning models and select the one that performed the best for this task.

---

## **3. Data Collection**

### **Web Scraping with Selenium and BeautifulSoup**

I used **Selenium** and **BeautifulSoup** to scrape job listings from the [Hiredly](https://my.hiredly.com/jobs) website. The following fields were scraped from each job listing:
- **Job Title**
- **Location**
- **Salary**
- **Job Type**
- **Job URL** (for reference, later dropped)

### **Script Used:**
The `scrape_jobs.py` script was used to scrape job data from the first 40 pages of the listing. The script automatically navigated through the pages and extracted the relevant fields.

---

## **4. Data Cleaning**

### **Cleaning Steps:**

1. **Remove Missing Values**: Rows where the **Job Type** or **Salary** fields were missing were removed.
2. **Drop 'Undisclosed' Salaries**: Rows where the salary was marked as **Undisclosed** were dropped.
3. **Processing Salary Values**: Salaries provided as a range (e.g., "RM 2500 - RM 2800") were averaged. Salaries in shorthand form (e.g., "5K") were expanded to full values (e.g., "5000").
4. **Drop Irrelevant Columns**: The **Job URL** column was dropped as it was not needed for prediction.

### **Data Cleaning Script:**
The `data_cleaning.py` script handled all of these cleaning steps.

---

## **5. Machine Learning Models**

### **Models Used:**
1. **Random Forest Regressor**: A powerful ensemble method that creates multiple decision trees and averages their predictions to improve accuracy.
2. **XGBoost Regressor**: An efficient and scalable implementation of gradient boosting for regression tasks.

### **Label Encoding:**
Since the dataset contains categorical features (e.g., Job Title, Location, and Job Type), **Label Encoding** was applied to convert the categorical data into numerical values. This encoding was applied to both training and prediction phases to ensure consistency.

---

## **6. Model Training and Evaluation**

Two models were trained and evaluated using the **Mean Squared Error (MSE)** and **R-squared (R²)** metrics. The dataset was split into training and testing sets (80% training, 20% testing).

### **Results:**

| Model          | Mean Squared Error (MSE) | R-squared (R²) |
|----------------|--------------------------|----------------|
| **Random Forest** | 3,638,780.55               | 0.3730         |
| **XGBoost**       | 4,127,546.84               | 0.2888         |

- **Random Forest** performed slightly better than **XGBoost**, with a lower MSE and higher R², indicating it explained more variance in the salary data.

### **Scripts Used:**
- **`model_training_random_forest.py`**: For Random Forest training.
- **`model_training_xgboost.py`**: For XGBoost training.

---

## **7. Predictions**

Once the models were trained, they were used to predict the salary for a sample job posting:
- **Job Title**: Software Engineer
- **Location**: Kuala Lumpur
- **Job Type**: Permanent

### **Prediction Results:**

| Model           | Predicted Salary         |
|-----------------|--------------------------|
| **Random Forest** | RM 6249.60               |
| **XGBoost**       | RM 6044.16               |

Both models produced similar salary predictions, with Random Forest predicting slightly higher.

### **Scripts Used:**
- **`model_prediction_comparison.py`**: Used to compare the predictions from both models.

---

## **8. Conclusion**

This project successfully demonstrated the process of building and comparing machine learning models for salary prediction based on categorical job features. While the **Random Forest** model performed slightly better, both models provided reasonable salary predictions. Further improvements could be made through hyperparameter tuning and by incorporating additional features such as **Experience Level** or **Company Size**.

---

## **9. Future Work**

To improve the model’s performance, the following steps could be considered:
- **Hyperparameter Tuning**: Fine-tuning the hyperparameters of the models to achieve better performance.
- **Feature Engineering**: Adding more relevant features like **Experience Level**, **Industry**, or **Company Size** could increase the model's accuracy.
- **Cross-Validation**: Implementing cross-validation techniques to ensure the model’s performance is stable across different subsets of data.

---

### **Final Remarks**

This project provides a complete end-to-end example of web scraping, data cleaning, machine learning model training, and prediction, making it a strong portfolio piece for showcasing skills in data science and machine learning.

---
