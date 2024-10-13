import pandas as pd
import joblib

# Load the label encoders (used for encoding categorical features)
label_encoders = joblib.load('label_encoders.pkl')

# Load the trained models
random_forest_model = joblib.load('salary_prediction_model_random_forest.pkl')
xgboost_model = joblib.load('salary_prediction_model_xgboost.pkl')

# Create new job data for prediction
new_data = pd.DataFrame({
    'Job Title': ['Software Engineer'],
    'Location': ['Kuala Lumpur'],
    'Job Type': ['Full-Time']  # Use valid categories seen during training
})

# Apply label encoding to new data
categorical_columns = ['Job Title', 'Location', 'Job Type']
for column in categorical_columns:
    new_data[column] = label_encoders[column].transform(new_data[column])

# Make predictions using the Random Forest model
rf_salary_pred = random_forest_model.predict(new_data)
print(f'Predicted Salary (Random Forest): {rf_salary_pred[0]}')

# Make predictions using the XGBoost model
xgb_salary_pred = xgboost_model.predict(new_data)
print(f'Predicted Salary (XGBoost): {xgb_salary_pred[0]}')
