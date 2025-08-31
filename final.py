import streamlit as st
import pandas as pd
import json
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.metrics import classification_report, confusion_matrix

# Setup
st.set_page_config(page_title="Insurance AI Dashboard", layout="wide")
st.title("📊 Unified Insurance Analytics Dashboard")

# --- Tabs for Navigation ---
tab1, tab2, tab3 = st.tabs(["📈 System Monitor", "🧭 MapReduce Insights", "🤖 Underwriting ML"])

# ------------------------------
# 🔧 TAB 1: System Monitor
# ------------------------------
with tab1:
    st.header("📈 System Performance During MapReduce Execution")
    try:
        with open("system_metrics.json", "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S')

        st.sidebar.header("🔧 System Monitor Controls")
        metric_selected = st.sidebar.multiselect("Select Metrics to View", ['CPU Usage', 'Memory Usage', 'Disk Usage', 'CPU Temperature'], default=['CPU Usage', 'Memory Usage'])

        if 'CPU Usage' in metric_selected:
            st.subheader("🔥 CPU Usage Over Time")
            st.altair_chart(alt.Chart(df).mark_line().encode(
                x='timestamp:T', y='cpu_usage:Q', tooltip=['timestamp:T', 'cpu_usage:Q']
            ).interactive(), use_container_width=True)

        if 'Memory Usage' in metric_selected:
            st.subheader("🧠 Memory Usage Over Time")
            st.altair_chart(alt.Chart(df).mark_line(color='green').encode(
                x='timestamp:T', y='memory_usage:Q', tooltip=['timestamp:T', 'memory_usage:Q']
            ).interactive(), use_container_width=True)

        if 'Disk Usage' in metric_selected:
            st.subheader("💾 Disk Usage Over Time")
            st.altair_chart(alt.Chart(df).mark_line(color='purple').encode(
                x='timestamp:T', y='disk_usage:Q', tooltip=['timestamp:T', 'disk_usage:Q']
            ).interactive(), use_container_width=True)

        if 'CPU Temperature' in metric_selected:
            st.subheader("🌡️ CPU Temperature Over Time (Simulated)")
            st.altair_chart(alt.Chart(df).mark_line(color='red').encode(
                x='timestamp:T', y='cpu_temp:Q', tooltip=['timestamp:T', 'cpu_temp:Q']
            ).interactive(), use_container_width=True)

        st.caption("Note: Temperature is simulated based on CPU load.")
    except FileNotFoundError:
        st.error("system_metrics.json not found. Please run your job with monitoring enabled.")

# ------------------------------
# 📊 TAB 2: MapReduce Results
# ------------------------------
with tab2:
    st.header("🧭 Insurance Underwriting MapReduce Analysis")
    def load_results():
        try:
            with open("insurance_mapreduce_results.json") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Failed to load results: {e}")
            return None

    results_data = load_results()
    if results_data:
        results = results_data["analysis_results"]
        st.markdown(f"**📅 Timestamp:** {results_data['timestamp']} | **🔢 Rows Processed:** {results_data['row_count']:,}")
        st.markdown("---")

        st.sidebar.header("🧭 MapReduce Dashboard Controls")

        # Churn by City
        churn_data = []
        for k, v in results.items():
            if k.startswith("churn_by_city_"):
                *_, city, reason = k.split("_")
                churn_data.append({"City Tier": city, "Churn Reason": reason, "Count": v})
        churn_df = pd.DataFrame(churn_data)
        city_sel = st.sidebar.multiselect("City Tier", churn_df["City Tier"].unique(), default=list(churn_df["City Tier"].unique()))
        reason_sel = st.sidebar.multiselect("Churn Reason", churn_df["Churn Reason"].unique(), default=list(churn_df["Churn Reason"].unique()))
        churn_df = churn_df[churn_df["City Tier"].isin(city_sel) & churn_df["Churn Reason"].isin(reason_sel)]

        st.subheader("1️⃣ Churn Reason by City Tier")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(px.bar(churn_df, x="City Tier", y="Count", color="Churn Reason", barmode="group"), use_container_width=True)
        with col2:
            st.plotly_chart(px.sunburst(churn_df, path=["City Tier", "Churn Reason"], values="Count"), use_container_width=True)

        # Risk Score
        risk_data = []
        for k, v in results.items():
            if k.startswith("risk_by_health_"):
                _, _, smoker, cond = k.split("_", 3)
                risk_data.append({"Smoker": smoker, "Condition": cond, "Average Risk Score": v})
        risk_df = pd.DataFrame(risk_data)
        smoker_sel = st.sidebar.radio("Smoker Type", risk_df["Smoker"].unique())
        risk_df = risk_df[risk_df["Smoker"] == smoker_sel]

        st.subheader("2️⃣ Risk Score by Smoker & Conditions")
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(px.bar(risk_df, x="Condition", y="Average Risk Score", color="Condition"), use_container_width=True)
        with col4:
            st.plotly_chart(px.pie(risk_df, names="Condition", values="Average Risk Score"), use_container_width=True)

        # Underwriting Decisions
        uw_data = []
        for k, v in results.items():
            if k.startswith("underwriting_"):
                _, inc, cred, dec = k.split("_", 3)
                uw_data.append({"Income Bracket": inc, "Credit Bracket": cred, "Decision": dec.capitalize(), "Count": v})
        uw_df = pd.DataFrame(uw_data)
        inc_sel = st.sidebar.multiselect("Income Bracket", uw_df["Income Bracket"].unique(), default=list(uw_df["Income Bracket"].unique()))
        cred_sel = st.sidebar.multiselect("Credit Score Bracket", uw_df["Credit Bracket"].unique(), default=list(uw_df["Credit Bracket"].unique()))
        uw_df = uw_df[(uw_df["Income Bracket"].isin(inc_sel)) & (uw_df["Credit Bracket"].isin(cred_sel))]

        st.subheader("3️⃣ Underwriting by Income & Credit Score")
        col5, col6 = st.columns(2)
        with col5:
            st.plotly_chart(px.bar(uw_df, x="Income Bracket", y="Count", color="Decision", facet_col="Credit Bracket"), use_container_width=True)
        with col6:
            st.plotly_chart(px.treemap(uw_df, path=["Credit Bracket", "Income Bracket", "Decision"], values="Count"), use_container_width=True)

        # Claims by Policy Term
        claims_data = []
        for k, v in results.items():
            if k.startswith("claims_by_term_"):
                term = int(k.split("_")[-1])
                claims_data.append({"Policy Term (Years)": term, "Total Claims": v["total_claims"], "Average Claims": v["average_claims"]})
        claims_df = pd.DataFrame(claims_data).sort_values("Policy Term (Years)")
        term_min, term_max = st.sidebar.slider("Policy Term Filter", min_value=int(claims_df["Policy Term (Years)"].min()),
                                               max_value=int(claims_df["Policy Term (Years)"].max()),
                                               value=(int(claims_df["Policy Term (Years)"].min()), int(claims_df["Policy Term (Years)"].max())))
        claims_df = claims_df[(claims_df["Policy Term (Years)"] >= term_min) & (claims_df["Policy Term (Years)"] <= term_max)]

        st.subheader("4️⃣ Claims by Policy Term")
        col7, col8 = st.columns(2)
        with col7:
            st.plotly_chart(px.line(claims_df, x="Policy Term (Years)", y="Total Claims", markers=True), use_container_width=True)
        with col8:
            fig8 = go.Figure()
            fig8.add_trace(go.Bar(x=claims_df["Policy Term (Years)"], y=claims_df["Average Claims"], marker_color="indigo"))
            fig8.update_layout(title="Average Claims by Policy Term", xaxis_title="Term", yaxis_title="Avg Claims")
            st.plotly_chart(fig8, use_container_width=True)

# ------------------------------
# 🤖 TAB 3: ML Underwriting
# ------------------------------
with tab3:
    st.header("🤖 ML Predictions: Automated Underwriting")

    uploaded_file = st.file_uploader("📥 Upload insurance dataset", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("📄 Dataset Preview")
        st.dataframe(df.head())

        true_churn = df['Churn'] if 'Churn' in df.columns else None
        df = df.drop(columns=['application_id', 'churn_reason'], errors='ignore')

        with open("underwriting_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        with open("label_encoders.pkl", "rb") as f:
            label_encoders = pickle.load(f)

        for col in df.select_dtypes(include='object').columns:
            if col in label_encoders:
                le = label_encoders[col]
                df[col] = df[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
                df[col] = le.transform(df[col])
            else:
                df[col] = df[col].astype('category').cat.codes

        X_scaled = scaler.transform(df.drop(columns=['Churn'], errors='ignore'))
        predicted = model.predict(X_scaled)
        df['Predicted_Churn'] = predicted

        if true_churn is not None:
            df['Churn'] = true_churn
            st.subheader("📊 Confusion Matrix")
            fig, ax = plt.subplots()
            sns.heatmap(confusion_matrix(df['Churn'], df['Predicted_Churn']), annot=True, fmt='d',
                        cmap="Blues", xticklabels=['Not Churn', 'Churn'], yticklabels=['Not Churn', 'Churn'])
            st.pyplot(fig)

            st.subheader("🧠 Classification Report")
            st.dataframe(pd.DataFrame(classification_report(df['Churn'], df['Predicted_Churn'], output_dict=True)).transpose())

        st.subheader("📌 Feature Importance")
        imp = pd.Series(model.feature_importances_, index=df.drop(columns=['Predicted_Churn', 'Churn'], errors='ignore').columns)
        st.bar_chart(imp.sort_values(ascending=False))

        st.subheader("🎯 Interactive Scatter Plot")
        num_cols = df.select_dtypes(include=['int64', 'float64']).columns.drop(['Predicted_Churn'], errors='ignore')
        x = st.selectbox("X-axis", num_cols)
        y = st.selectbox("Y-axis", num_cols, index=1)
        st.plotly_chart(px.scatter(df, x=x, y=y, color=df['Predicted_Churn'].map({0: "Not Churn", 1: "Churn"}),
                                   title=f"{x} vs {y}", symbol='Predicted_Churn'), use_container_width=True)

        st.download_button("📥 Download Predictions CSV", df.to_csv(index=False), file_name="predicted_churn.csv")
    else:
        st.info("Upload dataset to see predictions and analysis.")


