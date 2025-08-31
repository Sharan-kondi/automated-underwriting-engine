import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page setup
st.set_page_config(
    page_title="Insurance Underwriting Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Insurance Underwriting MapReduce Analysis Dashboard")

# Load JSON results
@st.cache_data
def load_results():
    try:
        with open("insurance_mapreduce_results.json") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

# Load data
results_data = load_results()
if not results_data:
    st.stop()

results = results_data["analysis_results"]
st.markdown(f"**📅 Timestamp:** {results_data['timestamp']} | **🔢 Rows Processed:** {results_data['row_count']:,}")

# Sidebar Filters
st.sidebar.header("🧭 Dashboard Controls")

# ---------- 1. Churn by City Tier ----------
st.header("1️⃣ Churn Reason by City Tier")
churn_data = []
for key, value in results.items():
    if key.startswith("churn_by_city_"):
        *_, city, churn = key.split("_")
        churn_data.append({"City Tier": city, "Churn Reason": churn, "Count": value})
churn_df = pd.DataFrame(churn_data)

selected_cities = st.sidebar.multiselect("City Tiers", churn_df["City Tier"].unique(), default=churn_df["City Tier"].unique())
selected_reasons = st.sidebar.multiselect("Churn Reasons", churn_df["Churn Reason"].unique(), default=churn_df["Churn Reason"].unique())
churn_df = churn_df[churn_df["City Tier"].isin(selected_cities) & churn_df["Churn Reason"].isin(selected_reasons)]

col1, col2 = st.columns(2)
with col1:
    fig1 = px.bar(churn_df, x="City Tier", y="Count", color="Churn Reason", barmode="group", title="Grouped Bar: Churn by City")
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    fig2 = px.sunburst(churn_df, path=["City Tier", "Churn Reason"], values="Count", title="Sunburst: City Tier & Churn Reason")
    st.plotly_chart(fig2, use_container_width=True)

# ---------- 2. Risk Score by Smoker & Conditions ----------
st.header("2️⃣ Risk Score by Smoker & Conditions")
risk_data = []
for key, value in results.items():
    if key.startswith("risk_by_health_"):
        _, _, smoker, condition = key.split("_", 3)
        risk_data.append({"Smoker": smoker, "Condition": condition, "Average Risk Score": value})
risk_df = pd.DataFrame(risk_data)

selected_smoker = st.sidebar.radio("Smoker Type", sorted(risk_df["Smoker"].unique()), index=0)
risk_df = risk_df[risk_df["Smoker"] == selected_smoker]

col3, col4 = st.columns(2)
with col3:
    fig3 = px.bar(risk_df, x="Condition", y="Average Risk Score", color="Condition", title="Bar: Risk Score by Condition")
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    fig4 = px.pie(risk_df, names="Condition", values="Average Risk Score", title="Pie: Risk Distribution by Condition")
    st.plotly_chart(fig4, use_container_width=True)

# ---------- 3. Underwriting by Income & Credit Score ----------
st.header("3️⃣ Underwriting by Income & Credit Score")
uw_data = []
for key, value in results.items():
    if key.startswith("underwriting_"):
        _, income, credit, decision = key.split("_", 3)
        uw_data.append({"Income Bracket": income, "Credit Bracket": credit, "Decision": decision.capitalize(), "Count": value})
uw_df = pd.DataFrame(uw_data)

income_selected = st.sidebar.multiselect("Income Brackets", uw_df["Income Bracket"].unique(), default=uw_df["Income Bracket"].unique())
credit_selected = st.sidebar.multiselect("Credit Score Brackets", uw_df["Credit Bracket"].unique(), default=uw_df["Credit Bracket"].unique())

filtered_uw_df = uw_df[
    (uw_df["Income Bracket"].isin(income_selected)) &
    (uw_df["Credit Bracket"].isin(credit_selected))
]

col5, col6 = st.columns(2)
with col5:
    fig5 = px.bar(filtered_uw_df, x="Income Bracket", y="Count", color="Decision", facet_col="Credit Bracket",
                  title="Facet Bar: Underwriting by Income & Credit")
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    fig6 = px.treemap(filtered_uw_df, path=["Credit Bracket", "Income Bracket", "Decision"], values="Count",
                      title="Treemap: Decisions by Income and Credit")
    st.plotly_chart(fig6, use_container_width=True)

# ---------- 4. Claims by Policy Term ----------
st.header("4️⃣ Claims by Policy Term")
claims_data = []
for key, value in results.items():
    if key.startswith("claims_by_term_"):
        term = key.split("_")[-1]
        claims_data.append({
            "Policy Term (Years)": int(term),
            "Total Claims": value["total_claims"],
            "Average Claims": value["average_claims"]
        })
claims_df = pd.DataFrame(claims_data).sort_values("Policy Term (Years)")

term_range = st.sidebar.slider("Policy Term Filter (Years)", min_value=int(claims_df["Policy Term (Years)"].min()),
                                max_value=int(claims_df["Policy Term (Years)"].max()),
                                value=(int(claims_df["Policy Term (Years)"].min()), int(claims_df["Policy Term (Years)"].max())))
claims_df = claims_df[
    (claims_df["Policy Term (Years)"] >= term_range[0]) &
    (claims_df["Policy Term (Years)"] <= term_range[1])
]

col7, col8 = st.columns(2)
with col7:
    fig7 = px.line(claims_df, x="Policy Term (Years)", y="Total Claims", markers=True, title="Line: Total Claims Over Policy Term")
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    fig8 = go.Figure()
    fig8.add_trace(go.Bar(x=claims_df["Policy Term (Years)"], y=claims_df["Average Claims"],
                          name="Average Claims", marker_color="indigo"))
    fig8.update_layout(title="Bar: Average Claims by Policy Term", xaxis_title="Term (Years)", yaxis_title="Avg Claims")
    st.plotly_chart(fig8, use_container_width=True)

# Footer
st.markdown("---")
st.success("✅ Dashboard loaded with rich visual insights and interactive controls.")
