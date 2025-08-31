# monitor_runner.py
import threading
import json
import os
import sys

# Add current and subdirectories to system path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ Correct local imports
from system_monitor import monitor_system
from mapreduce.insurance_mapreduce import run_insurance_mapreduce

system_metrics = []

def run_monitor():
    global system_metrics
    print("\n🌡️ System monitoring started...")
    system_metrics = monitor_system(interval=1, duration=30)
    print("🌡️ System monitoring finished.")

def run_job_with_monitoring():
    print("\n🛠️ Starting parallel system monitoring and insurance MapReduce job...\n")

    monitor_thread = threading.Thread(target=run_monitor)
    monitor_thread.start()

    run_insurance_mapreduce()

    monitor_thread.join()

    with open("system_metrics.json", "w") as f:
        json.dump(system_metrics, f, indent=2)

    print("\n📊 System metrics saved to 'system_metrics.json'")
    print("✅ Monitoring + MapReduce job complete.\n")

if __name__ == "__main__":
    run_job_with_monitoring()
