import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Buyer Segmentation Dashboard",
    layout="wide"
)

df = pd.read_csv("data/clustered_clients.csv")

st.title("🏠 Real Estate Buyer Segmentation Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Buyers", len(df))

with col2:
    st.metric(
        "Investors",
        len(df[df["acquisition_purpose"] == "Investment"])
    )

with col3:
    st.metric(
        "Companies",
        len(df[df["client_type"] == "Company"])
    )

with col4:
    st.metric(
        "Avg Satisfaction",
        round(df["satisfaction_score"].mean(), 2)
    )

st.write("Machine Learning Based Buyer Segmentation and Investment Profiling")

# Sidebar Filters
st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Country",
    ["All"] + sorted(df["country"].unique().tolist())
)

region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(df["region"].unique().tolist())
)

purpose = st.sidebar.selectbox(
    "Acquisition Purpose",
    ["All"] + sorted(df["acquisition_purpose"].unique().tolist())
)

client_type = st.sidebar.selectbox(
    "Client Type",
    ["All"] + sorted(df["client_type"].unique().tolist())
)

if country != "All":
    df = df[df["country"] == country]

if region != "All":
    df = df[df["region"] == region]

if purpose != "All":
    df = df[df["acquisition_purpose"] == purpose]

if client_type != "All":
    df = df[df["client_type"] == client_type]

# Segment Distribution
st.subheader("Buyer Segment Distribution")

fig = px.histogram(
    df,
    x="Segment",
    color="Segment"
)

st.plotly_chart(fig)

# Purpose Distribution
st.subheader("Acquisition Purpose")

fig2 = px.pie(
    df,
    names="acquisition_purpose"
)

st.plotly_chart(fig2)

# Loan Pattern
st.subheader("Loan Applied Analysis")

fig3 = px.histogram(
    df,
    x="loan_applied",
    color="Segment"
)

#Geographic Buyer Analysis
st.subheader("Geographic Buyer Analysis")

region_counts = (
    df.groupby(["region", "Segment"])
    .size()
    .reset_index(name="count")
)

fig4 = px.bar(
    region_counts,
    x="region",
    y="count",
    color="Segment",
    barmode="group"
)

st.plotly_chart(fig4)

#Investor Behavior Dashboard
st.subheader("Investor Behavior Dashboard")

fig5 = px.histogram(
    df,
    x="acquisition_purpose",
    color="Segment"
)

st.plotly_chart(fig5)

#segment insights
st.plotly_chart(fig3)

st.subheader("Segment Insights")

segment_summary = df.groupby("Segment").agg({
    "age": "mean",
    "satisfaction_score": "mean"
}).round(2)

st.dataframe(segment_summary)

# Data Preview
st.subheader("Dataset Preview")

st.dataframe(df.head())