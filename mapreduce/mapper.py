import csv
import json
import os
from collections import defaultdict
from multiprocessing import Pool
from datetime import datetime

# Task 1: Churn Reason by City Tier
class Task1_ChurnByCityMapper:
    def map(self, row):
        city_tier = row.get('city_tier', '').strip()
        churn_reason = row.get('churn_reason', '').strip()
        if city_tier and churn_reason:
            return [(f'churn_by_city_{city_tier}_{churn_reason}', 1)]
        return []


# Task 2: Risk Score by Smoker and Condition
class Task2_RiskByHealthMapper:
    def map(self, row):
        smoker = row.get('smoker', '').strip()
        existing_conditions = row.get('existing_conditions', '').strip()
        risk_score = float(row.get('risk_aversion_score', 0) or 0)
        if smoker and existing_conditions:
            return [(f'risk_by_health_{smoker}_{existing_conditions}', risk_score)]
        return []




# Task 3: Underwriting by Income and Credit Score
class Task3_UnderwritingMapper:
    def map(self, row):
        income = float(row.get('income', 0) or 0)
        credit_score = float(row.get('credit_score', 0) or 0)
        decision = row.get('underwriting_decision', '').strip().lower()
        income_bracket = 'low' if income < 30000 else 'med' if income < 70000 else 'high'
        credit_bracket = 'poor' if credit_score < 500 else 'fair' if credit_score < 700 else 'good'
        return [(f'underwriting_{income_bracket}_{credit_bracket}_{decision}', 1)]



# Task 4: Claims by Policy Term
class Task4_ClaimsByTermMapper:
    def map(self, row):
        term = int(row.get('policy_term_years', 0) or 0)
        claims = int(row.get('previous_claims', 0) or 0)
        return [(f'claims_by_term_{term}', claims)]








