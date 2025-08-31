# monitor_dashboard.py
import streamlit as st
import json
import pandas as pd
import altair as alt

st.set_page_config(page_title="System Monitor", layout="wide")

st.title("📊 System Performance During MapReduce Execution")

# Load data
try:
    with open("system_metrics.json", "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
except FileNotFoundError:
    st.error("system_metrics.json not found. Please run your job with monitoring.")
    st.stop()

# Convert timestamps
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S')

# Layout
col1, col2 = st.columns(2)

# 🔥 CPU Usage Chart
with col1:
    st.subheader("🔥 CPU Usage Over Time")
    chart = alt.Chart(df).mark_line().encode(
        x='timestamp:T',
        y='cpu_usage:Q',
        tooltip=['timestamp:T', 'cpu_usage:Q']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

# 🧠 Memory Usage Chart
with col2:
    st.subheader("🧠 Memory Usage Over Time")
    chart = alt.Chart(df).mark_line(color='green').encode(
        x='timestamp:T',
        y='memory_usage:Q',
        tooltip=['timestamp:T', 'memory_usage:Q']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

# 💾 Disk Usage Chart
st.subheader("💾 Disk Usage Over Time")
chart = alt.Chart(df).mark_line(color='purple').encode(
    x='timestamp:T',
    y='disk_usage:Q',
    tooltip=['timestamp:T', 'disk_usage:Q']
).interactive()
st.altair_chart(chart, use_container_width=True)

# 🌡️ CPU Temperature Chart
st.subheader("🌡️ CPU Temperature Over Time (Simulated)")
chart = alt.Chart(df).mark_line(color='red').encode(
    x='timestamp:T',
    y='cpu_temp:Q',
    tooltip=['timestamp:T', 'cpu_temp:Q']
).interactive()
st.altair_chart(chart, use_container_width=True)

st.caption("Note: Temperature is simulated based on CPU load.")
