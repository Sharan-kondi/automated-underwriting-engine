# run_mapreduce.py
import os
import subprocess
from resource_monitor import ResourceMonitor

monitor = ResourceMonitor()
print("🌡️ Starting system resource monitoring...")
monitor.start()

try:
    # Simulate a MapReduce pipeline
    print("🛠️ Running mapper...")
    with open("input.txt", "r") as infile, open("mapped.txt", "w") as outfile:
        subprocess.run(["python3", "mapper.py"], stdin=infile, stdout=outfile)

    print("🔁 Sorting...")
    subprocess.run(["sort", "mapped.txt", "-o", "sorted.txt"])

    print("🧠 Running reducer...")
    with open("sorted.txt", "r") as infile, open("output.txt", "w") as outfile:
        subprocess.run(["python3", "reducer.py"], stdin=infile, stdout=outfile)

finally:
    print("🛑 Stopping monitoring...")
    monitor.stop()
    print("✅ Job complete. Logs saved to 'mac_resource_log.csv'")
