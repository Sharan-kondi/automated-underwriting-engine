# predict_single.py

import pickle
import numpy as np
import pandas as pd

# --- Load model and preprocessing tools ---
with open("underwriting_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

# --- Define a customer likely to NOT churn ---
new_customer = {
    'age': 34,
    'gender': 'Female',
    'bmi': 23.0,
    'smoker': 'No',
    'income': 1200000,
    'occupation': 'Salaried',
    'marital_status': 'Married',
    'dependents': 1,
    'policy_term_years': 20,
    'coverage_amount': 3000000,
    'existing_conditions': 'None',  # Ensure same string format
    'previous_claims': 0,
    'application_channel': 'Agent',
    'underwriting_decision': 'Approved',
    'credit_score': 790,
    'education_level': 'Postgraduate',
    'employment_status': 'Employed',
    'residence_type': 'Owned',
    'city_tier': 'Tier 1',
    'risk_aversion_score': 9,
    'internet_usage_hours': 6.5,
    'phone_contact_frequency': 15
}

# --- Convert to DataFrame ---
df = pd.DataFrame([new_customer])

# --- Encode categorical features using saved encoders ---
for col in df.select_dtypes(include='object').columns:
    if col in label_encoders:
        le = label_encoders[col]
        if df[col].iloc[0] in le.classes_:
            df[col] = le.transform(df[col])
        else:
            # Handle unseen label by assigning most common class (safe fallback)
            print(f"⚠️ Unseen label '{df[col].iloc[0]}' in column '{col}', using fallback.")
            default_val = le.transform([le.classes_[0]])[0]
            df[col] = default_val
    else:
        df[col] = df[col].astype('category').cat.codes

# --- Scale numerical features ---
X_scaled = scaler.transform(df)

# --- Predict churn ---
prediction = model.predict(X_scaled)[0]
probability = model.predict_proba(X_scaled)[0][1]

# --- Output results ---
result = "Churn" if prediction == 1 else "Not Churn"
print(f"\n🔮 Prediction: {result}")
print(f"📊 Probability of churn: {probability * 100:.2f}%")
