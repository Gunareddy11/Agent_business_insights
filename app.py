# File: app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from dotenv import load_dotenv, find_dotenv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "agents"))


from agents.data_cleaning_agent import clean_data
from agents.eda_agent import generate_eda
from agents.insights_agent import generate_insights
from agents.recommendation_agent import generate_recommendations

# Load environment variables
_ = load_dotenv(find_dotenv())

st.set_page_config(page_title="AI Business Insights Agent", layout="wide")
st.title("📊 AI Business Insights Dashboard")

# --- File uploader ---
uploaded_file = st.file_uploader("Upload your CSV dataset", type=["csv"])
default_path = "data/sales_data_sample.csv"

try:
    if uploaded_file:
        df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
    else:
        df = pd.read_csv(default_path, encoding="ISO-8859-1")
except Exception as e:
    st.error(f"Error reading CSV: {e}")
    st.stop()

# Step 1: Data Cleaning
df = clean_data(df)

# --- Feature synonyms for flexible detection ---
feature_synonyms = {
    "sales": ["sales", "sale", "revenue", "profit", "amount", "total", "value"],
    "profit": ["profit", "margin", "gain", "income"],
    "region": ["region", "state", "area", "location", "market", "city", "district"],
    "product": ["product", "item", "category", "sku"]
}

def find_feature_column(df, synonyms):
    """Finds matching column name in dataset ignoring case & synonyms."""
    df_cols = {col.lower(): col for col in df.columns}
    for syn in synonyms:
        if syn.lower() in df_cols:
            return df_cols[syn.lower()]
    return None

# --- Detect columns dynamically ---
sales_col = find_feature_column(df, feature_synonyms["sales"])
profit_col = find_feature_column(df, feature_synonyms["profit"])
region_col = find_feature_column(df, feature_synonyms["region"])
product_col = find_feature_column(df, feature_synonyms["product"])

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filter Options")
regions = df[region_col].unique() if region_col else []
products = df[product_col].unique() if product_col else []

selected_region = st.sidebar.multiselect("Select Region", regions, default=regions)
selected_product = st.sidebar.multiselect("Select Product", products, default=products)

if region_col:
    df = df[df[region_col].isin(selected_region)]
if product_col:
    df = df[df[product_col].isin(selected_product)]

# --- KPIs ---
st.subheader("📌 Key Business Metrics")
col1, col2, col3 = st.columns(3)

total_sales = df[sales_col].sum() if sales_col else 0
avg_profit = df[profit_col].mean() if profit_col else 0
top_region = (
    df.groupby(region_col)[sales_col].sum().idxmax()
    if region_col and sales_col else "N/A"
)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Avg Profit", f"${avg_profit:,.0f}")
col3.metric("🌍 Top Region", top_region)

# --- Charts ---
st.subheader("📈 Visualizations")

# Sales trend over time if date column exists
date_col = next((c for c in df.columns if "date" in c.lower()), None)
if date_col and sales_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    sales_trend = df.groupby(date_col)[sales_col].sum().reset_index()
    fig = px.line(sales_trend, x=date_col, y=sales_col, title="Sales Trend Over Time")
    st.plotly_chart(fig, use_container_width=True)

# Region-wise sales
if region_col and sales_col:
    region_sales = df.groupby(region_col)[sales_col].sum().reset_index()
    fig = px.bar(region_sales, x=region_col, y=sales_col, title="Region-wise Sales", color=region_col)
    st.plotly_chart(fig, use_container_width=True)

# Product-wise sales
if product_col and sales_col:
    product_sales = df.groupby(product_col)[sales_col].sum().reset_index()
    fig = px.pie(product_sales, values=sales_col, names=product_col, title="Product-wise Sales Share")
    st.plotly_chart(fig, use_container_width=True)

# Profit vs Sales scatter
if sales_col and profit_col:
    fig = px.scatter(df, x=sales_col, y=profit_col, color=region_col if region_col else None,
                     title="Profit vs Sales")
    st.plotly_chart(fig, use_container_width=True)

# --- AI Insights ---
st.subheader("🔍 AI Insights")

# Generate insights dynamically using numeric & categorical columns
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

# Ensure sales/profit are prioritized if present
if sales_col and sales_col not in numeric_cols:
    numeric_cols.insert(0, sales_col)
if profit_col and profit_col not in numeric_cols:
    numeric_cols.insert(0, profit_col)

summary_stats = df[numeric_cols + categorical_cols].describe(include="all").to_string()
charts_info = f"Columns analyzed: {', '.join(numeric_cols + categorical_cols)}"

insights = generate_insights(summary_stats, charts_info)
st.write(insights)

# --- AI Recommendations ---
st.subheader("💡 AI Recommendations")
recommendations = generate_recommendations(insights)
st.write(recommendations)

