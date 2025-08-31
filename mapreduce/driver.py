import csv
import json
import os
from collections import defaultdict
from multiprocessing import Pool
from datetime import datetime

# Task 1: Churn Reason by City Tier
class Task1Driver:
    def run(self, rows):
        mapper = Task1_ChurnByCityMapper()
        reducer = Task1_ChurnByCityReducer()
        mapped = [pair for row in rows for pair in mapper.map(row)]
        return reducer.reduce(mapped)

# Task 2: Risk Score by Smoker and Condition
class Task2Driver:
    def run(self, rows):
        mapper = Task2_RiskByHealthMapper()
        reducer = Task2_RiskByHealthReducer()
        mapped = [pair for row in rows for pair in mapper.map(row)]
        return reducer.reduce(mapped)

# Task 3: Underwriting by Income and Credit Score
class Task3Driver:
    def run(self, rows):
        mapper = Task3_UnderwritingMapper()
        reducer = Task3_UnderwritingReducer()
        mapped = [pair for row in rows for pair in mapper.map(row)]
        return reducer.reduce(mapped)

# Task 4: Claims by Policy Term
class Task4Driver:
    def run(self, rows):
        mapper = Task4_ClaimsByTermMapper()
        reducer = Task4_ClaimsByTermReducer()
        mapped = [pair for row in rows for pair in mapper.map(row)]
        return reducer.reduce(mapped)

