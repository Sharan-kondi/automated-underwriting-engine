#Mapper class
class Task1_ChurnByCityMapper:
    def map(self, row):
        city_tier = row.get('city_tier', '').strip()
        churn_reason = row.get('churn_reason', '').strip()
        if city_tier and churn_reason:
            return [(f'churn_by_city_{city_tier}_{churn_reason}', 1)]
        return []

#Reducer class
class Task1_ChurnByCityReducer:
    def reduce(self, mapped_data):
        from collections import defaultdict
        result = defaultdict(int)
        for key, value in mapped_data:
            result[key] += value
        return dict(result)

#Driver class
class Task1Driver:
    def run(self, rows):
        mapper = Task1_ChurnByCityMapper()
        reducer = Task1_ChurnByCityReducer()
        mapped = [pair for row in rows for pair in mapper.map(row)]
        return reducer.reduce(mapped)