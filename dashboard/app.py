import pandas as pd
import streamlit as st

df = pd.read_parquet(
    "data/processed/users_processed.parquet"
)

st.set_page_config(
    page_title="TTC Digital Twin",
    layout="wide"
)

st.title("🚍 TTC Digital Twin")

st.metric(
    "Total Records",
    len(df)
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Preview")
    st.dataframe(df)

with col2:
    st.subheader("Email Domains")

    domains = (
        df["email"]
        .str.split("@")
        .str[1]
        .value_counts()
    )

    st.bar_chart(domains)