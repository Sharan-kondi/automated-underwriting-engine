#Mapper class
class Task2_RiskByHealthMapper:
    def map(self, row):
        smoker = row.get('smoker', '').strip()
        existing_conditions = row.get('existing_conditions', '').strip()
        risk_score = float(row.get('risk_aversion_score', 0) or 0)
        if smoker and existing_conditions:
            return [(f'risk_by_health_{smoker}_{existing_conditions}', risk_score)]
        return []

#Reducer class
class Task2_RiskByHealthReducer:
    def reduce(self, mapped_data):
        from collections import defaultdict
        grouped = defaultdict(list)
        for key, value in mapped_data:
            grouped[key].append(value)
        return {key: round(sum(values)/len(values), 2) for key, values in grouped.items() if values}

#Driver class
class Task2Driver:
    def run(self, rows):
        mapper = Task2_RiskByHealthMapper()
        reducer = Task2_RiskByHealthReducer()
        mapped = [pair for row in rows for pair in mapper.map(row)]
        return reducer.reduce(mapped)
        