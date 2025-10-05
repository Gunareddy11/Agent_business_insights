import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def generate_eda(df: pd.DataFrame):
    st.subheader("📊 Data Overview")
    st.write(df.describe())

    st.subheader("📈 Sales Trend Over Time")
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        sales_trend = df.groupby("date")["sales"].sum()
        st.line_chart(sales_trend)

    st.subheader("🏆 Top Products")
    if "product" in df.columns:
        top_products = df.groupby("product")["sales"].sum().sort_values(ascending=False).head(5)
        st.bar_chart(top_products)
