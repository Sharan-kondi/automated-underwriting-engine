# ml_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import xgboost as xgb
import pickle

# Load data
df = pd.read_csv('combined_life_insurance_with_churn_reason.csv')

# Clean columns
df.drop(columns=['application_id', 'churn_reason'], inplace=True, errors='ignore')

# Encode categorical features
label_encoders = {}
for col in df.select_dtypes(include='object').columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

# Slight noise on numerics
for col in ['income', 'credit_score', 'bmi', 'risk_aversion_score']:
    if col in df.columns:
        df[col] = df[col] * (1 + np.random.normal(0, 0.015, size=df.shape[0]))

# Split features/target
X = df.drop('Churn', axis=1)
y = df['Churn']

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Model with strong regularization
model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.05,
    subsample=0.6,
    colsample_bytree=0.6,
    reg_alpha=4,
    reg_lambda=2,
    gamma=2,
    use_label_encoder=False,
    eval_metric='logloss'
)

# Train
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"\n✅ Model Accuracy: {acc * 100:.2f}%")
print("\n📊 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\n🧠 Classification Report:")
print(classification_report(y_test, y_pred))

# Save artifacts
with open("underwriting_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
with open("label_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

print("\n💾 Model & preprocessors saved.")
