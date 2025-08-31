# streamlit_app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

# --- Load trained model and preprocessors ---
with open("underwriting_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

st.set_page_config(page_title="Underwriting Result Dashboard", layout="wide")
st.title("📊 Automated Underwriting Engine - Streamlit Dashboard")

uploaded_file = st.file_uploader("📥 Upload the life insurance dataset (no predictions needed)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Raw Dataset Preview")
    st.dataframe(df.head())

    # --- Save original churn column if exists ---
    true_churn = df['Churn'] if 'Churn' in df.columns else None

    # --- Drop unused columns ---
    df = df.drop(columns=['application_id', 'churn_reason'], errors='ignore')

    # --- Encode categorical features using saved label encoders ---
    for col in df.select_dtypes(include='object').columns:
        if col in label_encoders:
            le = label_encoders[col]
            df[col] = df[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
            df[col] = le.transform(df[col])
        else:
            df[col] = df[col].astype('category').cat.codes

    # --- Scale features ---
    X_scaled = scaler.transform(df.drop(columns=['Churn'], errors='ignore'))

    # --- Predict with model ---
    predicted = model.predict(X_scaled)
    df['Predicted_Churn'] = predicted

    # --- Add actual churn column if available ---
    if true_churn is not None:
        df['Churn'] = true_churn

        st.markdown("### 📊 Confusion Matrix")
        cm = confusion_matrix(df['Churn'], df['Predicted_Churn'])
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", xticklabels=['Not Churn', 'Churn'], yticklabels=['Not Churn', 'Churn'])
        st.pyplot(fig)

        st.markdown("### 🧠 Classification Report")
        report = classification_report(df['Churn'], df['Predicted_Churn'], output_dict=True)
        st.dataframe(pd.DataFrame(report).transpose())

    # --- Feature Importance ---
    st.markdown("### 📌 Feature Importance")
    feature_names = df.drop(columns=['Predicted_Churn', 'Churn'], errors='ignore').columns
    importances = pd.Series(model.feature_importances_, index=feature_names)
    st.bar_chart(importances.sort_values(ascending=False))

    # --- Interactive Scatter Plot ---
    st.markdown("### 🎯 Interactive Scatter Plot by Prediction")

    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.drop(['Predicted_Churn'], errors='ignore')
    x_axis = st.selectbox("Select X-axis", numerical_cols, index=0)
    y_axis = st.selectbox("Select Y-axis", numerical_cols, index=1)

    fig = px.scatter(
        df,
        x=x_axis,
        y=y_axis,
        color=df['Predicted_Churn'].map({0: "Not Churn", 1: "Churn"}),
        symbol='Predicted_Churn',
        title=f"{x_axis} vs {y_axis} (Colored by Prediction)",
        labels={'color': 'Prediction'},
        hover_data=['Predicted_Churn']
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Downloadable Result ---
    st.download_button("📥 Download Results CSV", df.to_csv(index=False), file_name="predicted_churn_results.csv")

else:
    st.info("👆 Please upload a clean dataset (same as used during training).")
