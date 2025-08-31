# regenerate_dataset.py

import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

N = 4000

# Feature generation
data = {
    'application_id': [f"AID{i:05d}" for i in range(N)],
    'age': np.random.randint(18, 65, size=N),
    'gender': np.random.choice(['Male', 'Female'], size=N),
    'bmi': np.round(np.random.normal(25, 5, N), 1),
    'smoker': np.random.choice(['Yes', 'No'], size=N, p=[0.3, 0.7]),
    'income': np.random.randint(100000, 1500000, size=N),
    'occupation': np.random.choice(['Salaried', 'Self-Employed', 'Unemployed'], N, p=[0.6, 0.3, 0.1]),
    'marital_status': np.random.choice(['Single', 'Married', 'Divorced'], N),
    'dependents': np.random.randint(0, 5, size=N),
    'policy_term_years': np.random.randint(5, 30, size=N),
    'coverage_amount': np.random.randint(100000, 10000000, size=N),
    'existing_conditions': np.random.choice(['None', 'Diabetes', 'Heart Disease', 'Cancer'], N, p=[0.6, 0.2, 0.15, 0.05]),
    'previous_claims': np.random.randint(0, 3, size=N),
    'application_channel': np.random.choice(['Agent', 'Online', 'Branch'], N),
    'underwriting_decision': np.random.choice(['Approved', 'Rejected', 'Review'], N, p=[0.8, 0.1, 0.1]),
    'credit_score': np.random.randint(300, 900, size=N),
    'education_level': np.random.choice(['High School', 'Graduate', 'Postgraduate'], N),
    'employment_status': np.random.choice(['Employed', 'Unemployed', 'Retired'], N),
    'residence_type': np.random.choice(['Owned', 'Rented'], N),
    'city_tier': np.random.choice(['Tier 1', 'Tier 2', 'Tier 3'], N, p=[0.5, 0.3, 0.2]),
    'risk_aversion_score': np.random.randint(1, 11, size=N),
    'internet_usage_hours': np.round(np.random.uniform(0.5, 10, size=N), 1),
    'phone_contact_frequency': np.random.randint(1, 20, size=N)
}

df = pd.DataFrame(data)

# Logical churn assignment
def generate_churn(row):
    score = 0
    if row['credit_score'] < 500: score += 1
    if row['smoker'] == 'Yes': score += 1
    if row['existing_conditions'] != 'None': score += 1
    if row['income'] < 300000: score += 1
    if row['risk_aversion_score'] < 4: score += 1
    if row['internet_usage_hours'] < 2: score += 1
    if row['phone_contact_frequency'] < 5: score += 1
    if row['city_tier'] == 'Tier 3': score += 1
    return 1 if score >= 3 else 0

df['Churn'] = df.apply(generate_churn, axis=1)

# Inject noise in 10% of labels
flip_indices = df.sample(frac=0.10, random_state=99).index
df.loc[flip_indices, 'Churn'] = df.loc[flip_indices, 'Churn'].apply(lambda x: 0 if x == 1 else 1)

# Add churn reasons
reasons = [
    "Premium too high", "Denied claim", "Switched to competitor",
    "Agent miscommunication", "Poor digital experience", "Life event change"
]
df['churn_reason'] = df['Churn'].apply(lambda x: random.choice(reasons) if x == 1 else '')

# Save
df.to_csv("combined_life_insurance_with_churn_reason.csv", index=False)
print("✅ Realistic dataset saved as 'combined_life_insurance_with_churn_reason.csv'")
