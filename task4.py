#Mapper class
class Task4_ClaimsByTermMapper:
    def map(self, row):
        term = int(row.get('policy_term_years', 0) or 0)
        claims = int(row.get('previous_claims', 0) or 0)
        return [(f'claims_by_term_{term}', claims)]
#Reducer class
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
#Driver class
class Task4Driver:
    def run(self, rows):
        mapper = Task4_ClaimsByTermMapper()
        reducer = Task4_ClaimsByTermReducer()
        mapped = [pair for row in rows for pair in mapper.map(row)]
        return reducer.reduce(mapped)
        