# Automated Underwriting Engine using Big Data and ML  

🚀 **Transforming traditional insurance underwriting with Big Data and Machine Learning.**  

---

## 📌 Project Overview  
The insurance industry is constrained by outdated, manual underwriting practices that are slow, inconsistent, and prone to errors. This project develops a **real-time Automated Underwriting Engine** that leverages **Big Data technologies (Hadoop, Spark, AWS EMR)** and **Machine Learning models (Random Forest, XGBoost, Logistic Regression, etc.)** to:  

- Automate risk scoring and underwriting decisions.  
- Enhance decision accuracy and fraud detection.  
- Enable scalable analytics on large volumes of insurance application data.  
- Provide real-time, interactive visualizations via a **Streamlit dashboard**.  

---

## 🎯 Objectives  
- Reduce manual underwriting workload with intelligent automation.  
- Deliver faster and more consistent underwriting decisions.  
- Improve customer experience with real-time processing.  
- Support insurers with insights into churn, claims, and risk factors.  

---

## 📊 Dataset
-We use a synthetic but realistic dataset “Combined Life Insurance with Churn Reason” that captures:
-Demographics: Age, gender, marital status, dependents, city tier.
-Health & Lifestyle: BMI, smoking status, existing conditions.
-Financials: Income, credit score, employment status, residence type.
-Policy Info: Policy term, coverage amount, claims history.
-Behavioral: Internet usage, phone contact frequency, churn reason.
-Data preprocessing includes imputation, outlier treatment, encoding, and feature engineering.

---

## ⚙️ Methodology
-Big Data Analytics (MapReduce & Spark):
Churn reason distribution by city tier.
Health risk segmentation.
Underwriting decisions by income & credit score.
Claims analysis by policy term.

-Machine Learning Models:
Logistic Regression (baseline).
Decision Tree (rule-based interpretability).
Random Forest (ensemble).
XGBoost (best performer with 91.2% accuracy, ROC-AUC 0.94).

-Visualization & Dashboard (Streamlit):
Upload new applicant data.
Generate underwriting predictions.
Visualize churn, claims, and decision insights.

---

## 🏗️ System Architecture
-Data Storage: Hadoop HDFS, AWS S3.
-Distributed Processing: Hadoop MapReduce, Apache Spark.
-Model Training & Serving: Scikit-learn, XGBoost, Flask APIs.
-Dashboard: Streamlit for interactive analytics.
-Deployment: AWS EMR, EC2, CloudWatch.

---

## 📈 Results
-91.2% accuracy with XGBoost.
-Churn insights segmented by city tiers (urban price sensitivity vs. rural agent influence).
-Risk profiling based on income, credit score, and health factors.

Streamlit dashboard enables real-time, interpretable decisions.
-
