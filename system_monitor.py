# system_monitor.py
import psutil
import time
from datetime import datetime

def monitor_system(interval=1, duration=30):
    """
    Monitor CPU, memory, disk usage, and temperature at regular intervals.
    Returns a list of recorded data points.
    """
    data = []

    for _ in range(int(duration / interval)):
        timestamp = datetime.now().strftime("%H:%M:%S")
        cpu_usage = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        # Get CPU temperature if available (may not work on macOS)
        try:
            temp = psutil.sensors_temperatures().get('coretemp', [{}])[0].get('current', None)
        except Exception:
            temp = None

        data.append({
            'timestamp': timestamp,
            'cpu_usage': cpu_usage,
            'memory_usage': memory,
            'disk_usage': disk,
            'cpu_temp': temp
        })

        time.sleep(interval)

    return data
