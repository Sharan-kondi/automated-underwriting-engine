# synth_temp_generator.py
import json
import random

def simulate_temp(cpu_usage):
    """Generate synthetic temperature based on CPU usage."""
    base_temp = 45  # Idle base
    max_temp = 85   # Max expected
    simulated = base_temp + (cpu_usage / 100.0) * (max_temp - base_temp)
    noise = random.uniform(-2, 2)
    return round(simulated + noise, 1)

with open("system_metrics.json", "r") as f:
    data = json.load(f)

for point in data:
    if point["cpu_temp"] is None:
        point["cpu_temp"] = simulate_temp(point["cpu_usage"])

with open("system_metrics.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Synthetic CPU temperatures added.")
