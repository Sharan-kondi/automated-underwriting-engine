import csv
import json
import os
from collections import defaultdict
from multiprocessing import Pool
from datetime import datetime

# Task 1: Churn Reason by City Tier
class Task1_ChurnByCityReducer:
    def reduce(self, mapped_data):
        from collections import defaultdict
        result = defaultdict(int)
        for key, value in mapped_data:
            result[key] += value
        return dict(result)
        
# Task 2: Risk Score by Smoker and Condition
class Task2_RiskByHealthReducer:
    def reduce(self, mapped_data):
        from collections import defaultdict
        grouped = defaultdict(list)
        for key, value in mapped_data:
            grouped[key].append(value)
        return {key: round(sum(values)/len(values), 2) for key, values in grouped.items() if values}



# Task 3: Underwriting by Income and Credit Score
class Task3_UnderwritingReducer:
    def reduce(self, mapped_data):
        from collections import defaultdict
        result = defaultdict(int)
        for key, value in mapped_data:
            result[key] += value
        return dict(result)



# Task 4: Claims by Policy Term
class Task4_ClaimsByTermReducer:
    def reduce(self, mapped_data):
        from collections import defaultdict
        grouped = defaultdict(list)
        for key, value in mapped_data:
            grouped[key].append(value)
        return {
            key: {
                "total_claims": sum(values),
                "average_claims": round(sum(values)/len(values), 2)
            } for key, values in grouped.items() if values
        }



