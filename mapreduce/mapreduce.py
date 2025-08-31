import csv
import json
import os
from collections import defaultdict
from multiprocessing import Pool
from datetime import datetime


# --- Config ---
CSV_FILE = 'combined_life_insurance_with_churn_reason.csv'
RESULTS_FILE = 'insurance_mapreduce_results.json'
ROW_LIMIT = 10000  # Adjust for testing or full run


# --- Check and read headers ---
def print_csv_headers():
    if not os.path.exists(CSV_FILE):
        print(f"\n❌ File not found: {CSV_FILE}")
        print("📌 Make sure the path is correct and the file exists.")
        exit(1)

    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        print("\n📄 Headers in CSV file:", header)
        return header


# --- Mapper Function ---
def map_insurance_features(row):
    try:
        city_tier = row.get('city_tier', '').strip()
        churn_reason = row.get('churn_reason', '').strip()
        smoker = row.get('smoker', '').strip()
        existing_conditions = row.get('existing_conditions', '').strip()
        risk_score = float(row.get('risk_aversion_score', 0) or 0)
        income = float(row.get('income', 0) or 0)
        credit_score = float(row.get('credit_score', 0) or 0)
        underwriting_decision = row.get('underwriting_decision', '').strip().lower()
        policy_term = int(row.get('policy_term_years', 0) or 0)
        previous_claims = int(row.get('previous_claims', 0) or 0)

        results = []

        # Task 1: Churn Reason by City Tier
        if city_tier and churn_reason:
            results.append((f'churn_by_city_{city_tier}_{churn_reason}', 1))

        # Task 2: Risk Score by Smoker and Condition
        if smoker and existing_conditions:
            results.append((f'risk_by_health_{smoker}_{existing_conditions}', risk_score))

        # Task 3: Underwriting by Income & Credit Score
        income_bracket = "low" if income < 30000 else "med" if income < 70000 else "high"
        credit_bracket = "poor" if credit_score < 500 else "fair" if credit_score < 700 else "good"
        results.append((f'underwriting_{income_bracket}_{credit_bracket}_{underwriting_decision}', 1))

        # Task 4: Claims by Policy Term
        results.append((f'claims_by_term_{policy_term}', previous_claims))

        return results
    except Exception as e:
        print(f"⚠️ Error processing row: {e}")
        return []


# --- Reducer Function ---
def reduce_insurance_data(mapped_data):
    summary = defaultdict(list)

    for key, value in mapped_data:
        summary[key].append(value)

    results = {}

    for key, values in summary.items():
        if key.startswith('risk_by_health_'):
            avg = sum(values) / len(values) if values else 0
            results[key] = round(avg, 2)
        elif key.startswith('claims_by_term_'):
            total = sum(values)
            count = len(values)
            results[key] = {
                "total_claims": total,
                "average_claims": round(total / count, 2)
            }
        else:
            results[key] = sum(values)

    return results


# --- Save results to JSON ---
def save_results_to_json(results, headers, row_count):
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'row_count': row_count,
        'headers': headers,
        'analysis_results': results
    }
    with open(RESULTS_FILE, 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"\n✅ Results saved to '{RESULTS_FILE}'")


# --- Print Task-wise Breakdown ---
def print_categorized_results(results):
    print("\n📊 TASK-WISE RESULTS")
    print("=" * 65)

    def print_section(title, condition):
        print(f"\n📌 {title}")
        print("-" * 65)
        filtered = {k: v for k, v in results.items() if condition(k)}
        if not filtered:
            print("No data available.")
        else:
            for k, v in sorted(filtered.items())[:10]:
                print(f"{k}: {v}")

    print_section("Task 1: Churn Reason by City Tier", lambda k: k.startswith("churn_by_city_"))
    print_section("Task 2: Risk Score by Smoker & Condition", lambda k: k.startswith("risk_by_health_"))
    print_section("Task 3: Underwriting Decisions by Income & Credit", lambda k: k.startswith("underwriting_"))
    print_section("Task 4: Claims by Policy Term", lambda k: k.startswith("claims_by_term_"))


# --- Main Execution ---
def run_insurance_mapreduce():
    print("\n📊 Starting Insurance Underwriting MapReduce Analysis")
    print("=" * 65)

    headers = print_csv_headers()

    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [row for i, row in enumerate(reader) if i < ROW_LIMIT]

    print(f"\n🔍 Processing {len(rows)} rows...")

    with Pool() as pool:
        mapped = pool.map(map_insurance_features, rows)

    flat_mapped = [item for sublist in mapped for item in sublist if sublist]
    reduced = reduce_insurance_data(flat_mapped)

    save_results_to_json(reduced, headers, len(rows))

    print("\n📌 SAMPLE SUMMARY OF ANALYSIS (Top 20)")
    print("=" * 65)
    for key, value in list(reduced.items())[:20]:
        print(f"{key}: {value}")

    print_categorized_results(reduced)
    print("\n✅ MapReduce execution complete.\n")


# --- Run ---
if __name__ == "__main__":
    run_insurance_mapreduce()
