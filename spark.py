import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator, MulticlassClassificationEvaluator, BinaryClassificationEvaluator

# --- Config ---
CSV_FILE = "/Users/aaditya/Desktop/sharan bdt project/data/combined_life_insurance_with_churn_reason.csv"

st.set_page_config(page_title="Insurance ML Dashboard", layout="wide")
st.title("📊 Insurance Risk & Decision Intelligence (Spark ML Dashboard)")

# --- Start Spark ---
@st.cache_resource
def create_spark():
    return SparkSession.builder.appName("UnderwritingML").getOrCreate()

spark = create_spark()

# --- Load Dataset ---
df = spark.read.csv(CSV_FILE, header=True, inferSchema=True).dropna()
df = df.withColumn("churn_reason", when(col("churn_reason") == "", None).otherwise(col("churn_reason")))
df = df.dropna(subset=["churn_reason", "city_tier", "smoker", "existing_conditions", 
                       "risk_aversion_score", "income", "credit_score", 
                       "underwriting_decision", "policy_term_years", "previous_claims"])

# --- Feature Engineering ---
df = df.withColumn("risk_score", col("risk_aversion_score").cast("double"))
df = df.withColumn("previous_claims", col("previous_claims").cast("int"))

# --- Task 1: Churn Reason by City Tier (Classification) ---
st.header("1️⃣ Churn Reason Prediction by City Tier")
try:
    indexer1 = StringIndexer(inputCols=["city_tier", "churn_reason"], outputCols=["city_idx", "churn_idx"]).fit(df)
    data1 = indexer1.transform(df)
    assembler1 = VectorAssembler(inputCols=["city_idx"], outputCol="features")
    assembled1 = assembler1.transform(data1)

    train1, test1 = assembled1.randomSplit([0.8, 0.2], seed=42)
    rf1 = RandomForestClassifier(labelCol="churn_idx", featuresCol="features")
    model1 = rf1.fit(train1)
    pred1 = model1.transform(test1)

    evaluator1 = MulticlassClassificationEvaluator(labelCol="churn_idx", predictionCol="prediction", metricName="accuracy")
    acc1 = evaluator1.evaluate(pred1)
    st.metric("Churn Reason Accuracy", f"{acc1:.4f}")
    st.dataframe(pred1.select("city_tier", "churn_reason", "prediction").limit(10).toPandas())
except Exception as e:
    st.error(f"Error in churn prediction: {str(e)}")

# --- Task 2: Risk Score by Smoker & Condition (Regression) ---
st.header("2️⃣ Risk Score Prediction by Health Profile")
try:
    indexer2 = StringIndexer(inputCols=["smoker", "existing_conditions"], outputCols=["smoker_idx", "cond_idx"]).fit(df)
    data2 = indexer2.transform(df)
    assembler2 = VectorAssembler(inputCols=["smoker_idx", "cond_idx"], outputCol="features")
    assembled2 = assembler2.transform(data2)

    train2, test2 = assembled2.randomSplit([0.8, 0.2], seed=42)
    lr2 = LinearRegression(labelCol="risk_score", featuresCol="features")
    model2 = lr2.fit(train2)
    pred2 = model2.transform(test2)

    rmse2 = RegressionEvaluator(labelCol="risk_score", predictionCol="prediction", metricName="rmse").evaluate(pred2)
    st.metric("RMSE (Risk Score)", f"{rmse2:.4f}")
    st.dataframe(pred2.select("smoker", "existing_conditions", "risk_score", "prediction").limit(10).toPandas())
except Exception as e:
    st.error(f"Error in risk score prediction: {str(e)}")

# --- Task 3: Underwriting Decision Prediction (Binary Classification) ---
st.header("3️⃣ Underwriting Decision Prediction")
try:
    df = df.withColumn("underwriting_idx", when(col("underwriting_decision") == "approved", 1).otherwise(0))
    assembler3 = VectorAssembler(inputCols=["income", "credit_score"], outputCol="features")
    data3 = assembler3.transform(df)

    train3, test3 = data3.randomSplit([0.8, 0.2], seed=42)
    rf3 = RandomForestClassifier(labelCol="underwriting_idx", featuresCol="features")
    model3 = rf3.fit(train3)
    pred3 = model3.transform(test3)

    auc3 = BinaryClassificationEvaluator(labelCol="underwriting_idx").evaluate(pred3)
    st.metric("AUC (Underwriting)", f"{auc3:.4f}")
    st.dataframe(pred3.select("income", "credit_score", "underwriting_decision", "prediction").limit(10).toPandas())
except Exception as e:
    st.error(f"Error in underwriting prediction: {str(e)}")

# --- Task 4: Claims by Policy Term (Regression) ---
st.header("4️⃣ Claims Prediction by Policy Term")
try:
    assembler4 = VectorAssembler(inputCols=["policy_term_years"], outputCol="features")
    data4 = assembler4.transform(df)

    train4, test4 = data4.randomSplit([0.8, 0.2], seed=42)
    lr4 = LinearRegression(labelCol="previous_claims", featuresCol="features")
    model4 = lr4.fit(train4)
    pred4 = model4.transform(test4)

    rmse4 = RegressionEvaluator(labelCol="previous_claims", predictionCol="prediction", metricName="rmse").evaluate(pred4)
    st.metric("RMSE (Claims)", f"{rmse4:.4f}")
    st.dataframe(pred4.select("policy_term_years", "previous_claims", "prediction").limit(10).toPandas())
except Exception as e:
    st.error(f"Error in claims prediction: {str(e)}")

# --- End Spark ---
spark.stop()
st.success("✅ Spark ML dashboard executed successfully!")
