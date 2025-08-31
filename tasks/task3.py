#Mapper class
class Task3_UnderwritingMapper:
    def map(self, row):
        income = float(row.get('income', 0) or 0)
        credit_score = float(row.get('credit_score', 0) or 0)
        decision = row.get('underwriting_decision', '').strip().lower()
        income_bracket = 'low' if income < 30000 else 'med' if income < 70000 else 'high'
        credit_bracket = 'poor' if credit_score < 500 else 'fair' if credit_score < 700 else 'good'
        return [(f'underwriting_{income_bracket}_{credit_bracket}_{decision}', 1)]

#Reducer class
class Task3_UnderwritingReducer:
    def reduce(self, mapped_data):
        from collections import defaultdict
        result = defaultdict(int)
        for key, value in mapped_data:
            result[key] += value
        return dict(result)

#Driver class
class Task3Driver:
    def run(self, rows):
        mapper = Task3_UnderwritingMapper()
        reducer = Task3_UnderwritingReducer()
        mapped = [pair for row in rows for pair in mapper.map(row)]
        return reducer.reduce(mapped)
        