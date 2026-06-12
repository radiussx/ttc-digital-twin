from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TTC Digital Twin",
    layout="wide"
)

latest_file = max(
    Path("data/raw").glob("ttc_vehicles_*.parquet")
)

df = pd.read_parquet(latest_file)
df["vehicle_num"] = pd.to_numeric(
    df["vehicle_id"],
    errors="coerce"
)

df["vehicle_type"] = df["vehicle_num"].apply(
    lambda x: "Streetcar"
    if 4400 <= x <= 4699
    else "Bus"
)
streetcars = (
    df["vehicle_type"] == "Streetcar"
).sum()

buses = (
    df["vehicle_type"] == "Bus"
).sum()
active_routes = (
    df[df["route_id"] != ""]
    ["route_id"]
    .nunique()
)

st.title("🚍 TTC Digital Twin")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Active Vehicles",
        len(df)
    )

with col2:
    st.metric(
        "Active Routes",
        active_routes
    )
with col3:
    st.metric(
        "🚌 Buses",
        buses
    )

with col4:
    st.metric(
        "🚋 Streetcars",
        streetcars
    )
route_counts = (
    df[df["route_id"] != ""]
    .groupby("route_id")
    .size()
    .reset_index(name="vehicle_count")
    .sort_values(
        "vehicle_count",
        ascending=False
    )
)

route_names = pd.read_csv(
    "data/route_names.csv",
    dtype={"route_id": str}
)

route_counts["route_id"] = (
    route_counts["route_id"]
    .astype(str)
)

route_counts = route_counts.merge(
    route_names,
    on="route_id",
    how="left"
)

route_counts["display"] = (
    route_counts["route_id"]
    + " "
    + route_counts["route_name"].fillna("")
)



st.subheader("Top Routes by Vehicle Count")

st.dataframe(
    route_counts[
        ["display", "vehicle_count"]
    ].head(20)
)

st.subheader("Route Distribution")

chart_data = (
    route_counts
    .set_index("display")
    ["vehicle_count"]
    .head(20)
)

st.bar_chart(chart_data)

st.subheader("Live Vehicle Map")

st.map(
    df.rename(
        columns={
            "latitude": "lat",
            "longitude": "lon"
        }
    )[["lat", "lon"]]
)