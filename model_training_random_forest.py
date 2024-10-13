import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the cleaned data (without one-hot encoding)
data = pd.read_csv('cleaned_job_vacancies_data.csv')

# Initialize label encoders for categorical columns
label_encoders = {}
categorical_columns = ['Job Title', 'Location', 'Job Type']

# Apply label encoding to each categorical feature
for column in categorical_columns:
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])

# Split features and target variable
X = data.drop(columns=['Salary'])  # Features: Label-encoded Job Title, Location, Job Type
y = data['Salary']  # Target: Salary

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Save the trained model
joblib.dump(model, 'salary_prediction_model_random_forest.pkl')
print("Model saved to 'salary_prediction_model_random_forest.pkl'")

# Optionally save the label encoders for future use
joblib.dump(label_encoders, 'label_encoders.pkl')
