# streamlit_dashboard.py
import pandas as pd
import streamlit as st

st.title("🖥️ MapReduce Resource Monitor")

df = pd.read_csv("mac_resource_log.csv")
df['Time'] = pd.to_datetime(df['Time'])
df.set_index('Time', inplace=True)

st.line_chart(df[['CPU_Usage(%)', 'Memory_Usage(%)', 'Disk_Usage(%)']])
if 'CPU_Temp(C)' in df:
    st.line_chart(df[['CPU_Temp(C)']])
