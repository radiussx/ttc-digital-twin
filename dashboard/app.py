from datetime import datetime

import pandas as pd
import pydeck as pdk
import requests
import streamlit as st
from google.transit import gtfs_realtime_pb2
from streamlit_autorefresh import st_autorefresh


st.set_page_config(
    page_title="TTC Digital Twin",
    layout="wide"
)

# Refresh every 5 seconds
st_autorefresh(
    interval=5000,
    key="ttc_refresh"
)


@st.cache_data(ttl=5)
def get_live_ttc_data():

    url = "https://bustime.ttc.ca/gtfsrt/vehicles"

    response = requests.get(
        url,
        timeout=30
    )

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    rows = []

    for entity in feed.entity:

        if entity.HasField("vehicle"):

            vehicle = entity.vehicle

            rows.append({
                "vehicle_id": str(vehicle.vehicle.id),
                "route_id": str(vehicle.trip.route_id),
                "trip_id": str(vehicle.trip.trip_id),
                "latitude": vehicle.position.latitude,
                "longitude": vehicle.position.longitude,
            })

    return pd.DataFrame(rows)


# Load Data
df = get_live_ttc_data()

# Clean Coordinates
df["latitude"] = pd.to_numeric(
    df["latitude"],
    errors="coerce"
)

df["longitude"] = pd.to_numeric(
    df["longitude"],
    errors="coerce"
)

df = df.dropna(
    subset=["latitude", "longitude"]
)

# Header
st.title("🚍 TTC Digital Twin")

st.caption(
    f"Live TTC Feed • Updated: {datetime.now().strftime('%H:%M:%S')}"
)

# Filters
route_options = sorted(
    [
        route
        for route in df["route_id"].unique()
        if route.strip() != ""
    ]
)

selected_route = st.selectbox(
    "Select Route",
    ["All Routes"] + route_options
)

if selected_route != "All Routes":

    df = df[
        df["route_id"] == selected_route
    ]

vehicle_search = st.text_input(
    "Track Vehicle ID"
)

if vehicle_search:

    df = df[
        df["vehicle_id"]
        .str.contains(
            vehicle_search,
            na=False
        )
    ]

# KPI Cards
col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🚍 Active Vehicles",
        len(df)
    )

with col2:

    st.metric(
        "🛣 Active Routes",
        df["route_id"].nunique()
    )

with col3:

    st.metric(
        "🎫 Active Trips",
        df["trip_id"].nunique()
    )

# Route Table
st.subheader("🏆 Top Routes By Vehicle Count")

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

st.dataframe(
    route_counts.head(20),
    use_container_width=True
)

# Route Chart
st.subheader("📊 Route Distribution")

chart_data = (
    route_counts
    .set_index("route_id")
    ["vehicle_count"]
    .head(20)
)

st.bar_chart(chart_data)

# LIVE MAP
st.subheader("🗺️ Live TTC Vehicle Map")

view_state = pdk.ViewState(
    latitude=float(df["latitude"].mean()),
    longitude=float(df["longitude"].mean()),
    zoom=10,
)

vehicle_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["longitude", "latitude"],
    get_fill_color=[255, 0, 0, 220],
    get_radius=120,
    pickable=True,
)

deck = pdk.Deck(
    initial_view_state=view_state,
    layers=[vehicle_layer],
    tooltip={
        "html": """
        <b>🚍 Vehicle:</b> {vehicle_id}<br/>
        <b>🛣 Route:</b> {route_id}<br/>
        <b>🎫 Trip:</b> {trip_id}<br/>
        <b>📍 Lat:</b> {latitude}<br/>
        <b>📍 Lon:</b> {longitude}
        """,
        "style": {
            "backgroundColor": "#1f2937",
            "color": "white"
        }
    }
)

st.pydeck_chart(
    deck,
    use_container_width=True
)

# Raw Data
with st.expander("View Raw TTC Data"):

    st.dataframe(
        df,
        use_container_width=True
    )