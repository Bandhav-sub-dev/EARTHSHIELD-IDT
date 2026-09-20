
import os
import json
import math
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
import numpy as np
import pandas as pd
import streamlit as st
import folium

from folium.plugins import HeatMap
from streamlit_folium import st_folium


# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT = Path("/content/EARTHSHIELD")
DATA_DIR = PROJECT / "data"
PROCESSED_DIR = DATA_DIR / "processed"

USGS_URL = (
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"
    "all_day.geojson"
)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="EARTHSHIELD | Disaster Command Center",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============================================================================
# DARK COMMAND CENTER UI
# =============================================================================

st.markdown(
    """
<style>

html, body, [class*="css"] {
    font-family: Inter, Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(40, 80, 120, 0.16),
            transparent 32%
        ),
        radial-gradient(
            circle at bottom left,
            rgba(130, 30, 30, 0.12),
            transparent 30%
        ),
        #070b12;
    color: #e9eef5;
}

section[data-testid="stSidebar"] {
    background: #090e16;
    border-right: 1px solid #202a36;
}

section[data-testid="stSidebar"] * {
    color: #dce5ef;
}

h1, h2, h3 {
    color: #f4f7fb;
}

.esh-header {
    background:
        linear-gradient(
            135deg,
            rgba(17, 26, 39, 0.98),
            rgba(7, 13, 22, 0.98)
        );
    border: 1px solid #263343;
    border-left: 4px solid #e53935;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.esh-title {
    font-size: 32px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.esh-subtitle {
    color: #8fa3b8;
    font-size: 14px;
    margin-top: 4px;
}

.status-online {
    color: #37d67a;
    font-weight: 700;
}

.status-warning {
    color: #ffb84d;
    font-weight: 700;
}

.status-danger {
    color: #ff5b5b;
    font-weight: 700;
}

.metric-card {
    background: linear-gradient(145deg, #101824, #0b111a);
    border: 1px solid #263343;
    border-radius: 10px;
    padding: 15px;
    min-height: 100px;
}

.metric-label {
    color: #7f93a8;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    color: #f5f7fa;
    font-size: 27px;
    font-weight: 800;
    margin-top: 5px;
}

.metric-small {
    color: #91a3b7;
    font-size: 11px;
    margin-top: 4px;
}

.section-title {
    font-size: 18px;
    font-weight: 750;
    color: #edf2f7;
    margin: 15px 0 8px 0;
}

.alert-critical {
    border-left: 4px solid #ff3b30;
    background: rgba(255,59,48,0.08);
    padding: 10px;
    border-radius: 7px;
    margin-bottom: 7px;
}

.alert-high {
    border-left: 4px solid #ff9500;
    background: rgba(255,149,0,0.08);
    padding: 10px;
    border-radius: 7px;
    margin-bottom: 7px;
}

.alert-moderate {
    border-left: 4px solid #ffd60a;
    background: rgba(255,214,10,0.06);
    padding: 10px;
    border-radius: 7px;
    margin-bottom: 7px;
}

.footer {
    color: #607287;
    font-size: 11px;
    text-align: center;
    padding: 20px;
}

div[data-testid="stMetric"] {
    background: #101824;
    border: 1px solid #263343;
    padding: 10px;
    border-radius: 9px;
}

</style>
""",
    unsafe_allow_html=True
)


# =============================================================================
# INDIA REFERENCE LOCATIONS
# =============================================================================

INDIA_LOCATIONS = {
    "New Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Ahmedabad": (23.0225, 72.5714),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Bhopal": (23.2599, 77.4126),
    "Patna": (25.5941, 85.1376),
    "Guwahati": (26.1445, 91.7362),
    "Bhubaneswar": (20.2961, 85.8245),
    "Srinagar": (34.0837, 74.7973),
    "Dehradun": (30.3165, 78.0322),
    "Shimla": (31.1048, 77.1734),
    "Chandigarh": (30.7333, 76.7794),
    "Gandhinagar": (23.2156, 72.6369),
    "Thiruvananthapuram": (8.5241, 76.9366),
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

@st.cache_data(ttl=300, show_spinner=False)
def fetch_earthquakes():

    try:
        response = requests.get(
            USGS_URL,
            timeout=20,
            headers={"User-Agent": "EARTHSHIELD/Day3"}
        )

        response.raise_for_status()

        payload = response.json()

        rows = []

        for feature in payload.get("features", []):

            props = feature.get("properties", {})
            geometry = feature.get("geometry", {})
            coords = geometry.get("coordinates", [])

            if len(coords) < 2:
                continue

            longitude = coords[0]
            latitude = coords[1]
            depth = coords[2] if len(coords) > 2 else None

            magnitude = props.get("mag")

            if magnitude is None:
                magnitude = 0.0

            timestamp = props.get("time")

            event_time = None

            if timestamp:
                event_time = datetime.fromtimestamp(
                    timestamp / 1000,
                    tz=timezone.utc
                )

            rows.append(
                {
                    "id": feature.get("id"),
                    "place": props.get("place") or "Unknown location",
                    "magnitude": float(magnitude),
                    "latitude": latitude,
                    "longitude": longitude,
                    "depth_km": depth,
                    "time": event_time,
                    "url": props.get("url"),
                    "tsunami": props.get("tsunami", 0),
                    "felt": props.get("felt"),
                    "alert": props.get("alert"),
                }
            )

        return pd.DataFrame(rows)

    except Exception as exc:

        st.warning(
            f"Earthquake service unavailable: {exc}"
        )

        return pd.DataFrame(
            columns=[
                "id",
                "place",
                "magnitude",
                "latitude",
                "longitude",
                "depth_km",
                "time",
                "url",
                "tsunami",
                "felt",
                "alert",
            ]
        )


def haversine_km(lat1, lon1, lat2, lon2):

    radius = 6371.0

    p1 = math.radians(lat1)
    p2 = math.radians(lat2)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(p1)
        * math.cos(p2)
        * math.sin(dlon / 2) ** 2
    )

    return 2 * radius * math.asin(math.sqrt(a))


def classify_earthquake(magnitude, depth):

    if magnitude >= 7.0:
        return "CRITICAL"

    if magnitude >= 6.0:
        return "HIGH"

    if magnitude >= 5.0:
        return "ELEVATED"

    if magnitude >= 4.0:
        return "MODERATE"

    return "LOW"


def india_region_filter(df):

    if df.empty:
        return df

    # Always guarantee the derived severity field.
    # This prevents downstream map/table components from depending
    # on API-specific dataframe state.
    if "severity" not in df.columns:
        df = df.copy()

        if "magnitude" in df.columns:
            df["severity"] = df.apply(
                lambda r: classify_earthquake(
                    r.get("magnitude", 0.0),
                    r.get("depth_km")
                ),
                axis=1
            )

    # India + nearby seismic region.
    # Deliberately broader than political boundaries because
    # nearby earthquakes can affect India.
    mask = (
        (df["latitude"] >= 4)
        & (df["latitude"] <= 38)
        & (df["longitude"] >= 65)
        & (df["longitude"] <= 100)
    )

    return df.loc[mask].copy()


@st.cache_data(ttl=300, show_spinner=False)
def fetch_weather():

    rows = []

    for city, (lat, lon) in INDIA_LOCATIONS.items():

        try:

            params = {
                "latitude": lat,
                "longitude": lon,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "precipitation,"
                    "rain,"
                    "weather_code,"
                    "wind_speed_10m,"
                    "wind_direction_10m"
                ),
                "timezone": "Asia/Kolkata",
            }

            response = requests.get(
                OPEN_METEO_URL,
                params=params,
                timeout=15
            )

            response.raise_for_status()

            payload = response.json()
            current = payload.get("current", {})

            rows.append(
                {
                    "city": city,
                    "latitude": lat,
                    "longitude": lon,
                    "temperature": current.get("temperature_2m"),
                    "humidity": current.get("relative_humidity_2m"),
                    "apparent_temperature": current.get(
                        "apparent_temperature"
                    ),
                    "precipitation": current.get("precipitation"),
                    "rain": current.get("rain"),
                    "wind_speed": current.get("wind_speed_10m"),
                    "wind_direction": current.get(
                        "wind_direction_10m"
                    ),
                    "weather_code": current.get("weather_code"),
                }
            )

        except Exception:
            continue

    return pd.DataFrame(rows)


def weather_description(code):

    if code is None:
        return "Unknown"

    code = int(code)

    mapping = {
        0: "Clear",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Drizzle",
        55: "Heavy drizzle",
        61: "Light rain",
        63: "Rain",
        65: "Heavy rain",
        71: "Light snow",
        73: "Snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Rain showers",
        82: "Heavy showers",
        95: "Thunderstorm",
        96: "Thunderstorm + hail",
        99: "Thunderstorm + hail",
    }

    return mapping.get(code, "Unknown")


def weather_risk(row):

    score = 0

    rain = row.get("rain", 0) or 0
    wind = row.get("wind_speed", 0) or 0
    temp = row.get("temperature", 25) or 25
    code = row.get("weather_code")

    if rain >= 20:
        score += 3
    elif rain >= 5:
        score += 2
    elif rain > 0:
        score += 1

    if wind >= 70:
        score += 3
    elif wind >= 45:
        score += 2
    elif wind >= 30:
        score += 1

    if code in [95, 96, 99]:
        score += 3

    if temp >= 45 or temp <= 0:
        score += 2

    if score >= 5:
        return "HIGH"

    if score >= 3:
        return "MODERATE"

    return "LOW"


def severity_symbol(level):

    if level == "CRITICAL":
        return "🔴"

    if level == "HIGH":
        return "🟠"

    if level == "MODERATE":
        return "🟡"

    if level == "ELEVATED":
        return "🟡"

    return "🟢"


# =============================================================================
# DATA
# =============================================================================

earthquakes = fetch_earthquakes()
india_eq = india_region_filter(earthquakes)
weather = fetch_weather()

if not earthquakes.empty:
    earthquakes["severity"] = earthquakes.apply(
        lambda r: classify_earthquake(
            r["magnitude"],
            r["depth_km"]
        ),
        axis=1
    )

if not weather.empty:
    weather["risk"] = weather.apply(
        weather_risk,
        axis=1
    )

last_update = datetime.now().astimezone()


# =============================================================================
# HEADER
# =============================================================================

st.markdown(
    f"""
<div class="esh-header">

<div class="esh-title">
🌍 EARTHSHIELD
</div>

<div class="esh-subtitle">
DISASTER DETECTION & MONITORING COMMAND CENTER
</div>

<div style="margin-top:10px;color:#8fa3b8;font-size:12px;">
LIVE DATA SYSTEM &nbsp; • &nbsp;
EARTHQUAKES + WEATHER + GEO-MONITORING
&nbsp; • &nbsp;
LAST UPDATE: {last_update.strftime("%d %b %Y %H:%M:%S")}
</div>

</div>
""",
    unsafe_allow_html=True
)


# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.markdown("## 🌍 EARTHSHIELD")

st.sidebar.caption("Day 3 — Geospatial Command Center")

page = st.sidebar.radio(
    "MONITORING MODULE",
    [
        "Command Center",
        "Earthquake Monitor",
        "Weather Monitor",
        "Alert Center",
        "System Status",
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### MAP CONTROLS")

map_style = st.sidebar.selectbox(
    "Base map",
    [
        "Satellite",
        "Street",
        "Terrain",
    ]
)

show_earthquakes = st.sidebar.checkbox(
    "Earthquakes",
    value=True
)

show_weather = st.sidebar.checkbox(
    "Weather stations",
    value=True
)

show_heatmap = st.sidebar.checkbox(
    "Earthquake heatmap",
    value=True
)

st.sidebar.markdown("---")

refresh = st.sidebar.button(
    "🔄 REFRESH LIVE DATA",
    use_container_width=True
)

if refresh:
    st.cache_data.clear()
    st.rerun()

auto_refresh = st.sidebar.checkbox(
    "Auto refresh",
    value=False
)

refresh_seconds = st.sidebar.slider(
    "Refresh interval",
    min_value=30,
    max_value=300,
    value=60,
    step=30
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "DAY 3 BUILD\n"
    "Geospatial monitoring foundation"
)


# =============================================================================
# MAP CREATOR
# =============================================================================

def create_map():

    fmap = folium.Map(
        location=[22.5, 79.0],
        zoom_start=5,
        control_scale=True,
        tiles=None
    )

    # -------------------------------------------------------------------------
    # STREET
    # -------------------------------------------------------------------------

    folium.TileLayer(
        tiles="OpenStreetMap",
        name="Street",
        overlay=False,
        control=True
    ).add_to(fmap)

    # -------------------------------------------------------------------------
    # SATELLITE
    # -------------------------------------------------------------------------

    folium.TileLayer(
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ),
        attr="Esri World Imagery",
        name="Satellite",
        overlay=False,
        control=True
    ).add_to(fmap)

    # -------------------------------------------------------------------------
    # TERRAIN
    # -------------------------------------------------------------------------

    folium.TileLayer(
        tiles=(
            "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
        ),
        attr="OpenTopoMap",
        name="Terrain",
        overlay=False,
        control=True
    ).add_to(fmap)

    # -------------------------------------------------------------------------
    # INDIA BOUNDING / MONITORING ZONE
    # -------------------------------------------------------------------------

    folium.Rectangle(
        bounds=[
            [7.5, 68.0],
            [35.5, 97.5]
        ],
        color="#3b82f6",
        weight=1,
        fill=False,
        tooltip="India monitoring zone"
    ).add_to(fmap)

    # -------------------------------------------------------------------------
    # EARTHQUAKE MARKERS
    # -------------------------------------------------------------------------

    if show_earthquakes and not india_eq.empty:

        for _, row in india_eq.iterrows():

            mag = float(row.get("magnitude", 0.0) or 0.0)

            # Defensive severity calculation.
            # Some API/dataframe paths may not contain the derived
            # "severity" column even though magnitude is available.
            if "severity" in row.index and pd.notna(row["severity"]):
                severity = str(row["severity"])
            else:
                severity = classify_earthquake(
                    mag,
                    row.get("depth_km")
                )

            if severity == "CRITICAL":
                radius = 16
                color = "#ff3030"

            elif severity == "HIGH":
                radius = 13
                color = "#ff8a00"

            elif severity in ["ELEVATED", "MODERATE"]:
                radius = 10
                color = "#ffd60a"

            else:
                radius = 7
                color = "#36d399"

            time_text = (
                row["time"].strftime("%Y-%m-%d %H:%M UTC")
                if pd.notna(row["time"])
                else "Unknown"
            )

            popup_html = f"""
            <div style="font-family:Arial;min-width:250px;">
                <h4>EARTHQUAKE EVENT</h4>
                <b>Magnitude:</b> {mag:.1f}<br>
                <b>Severity:</b> {severity}<br>
                <b>Location:</b> {row['place']}<br>
                <b>Depth:</b> {row['depth_km']:.1f} km<br>
                <b>Time:</b> {time_text}<br>
                <b>Tsunami flag:</b> {row['tsunami']}<br>
            </div>
            """

            folium.CircleMarker(
                location=[
                    row["latitude"],
                    row["longitude"]
                ],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.75,
                weight=2,
                popup=folium.Popup(
                    popup_html,
                    max_width=350
                ),
                tooltip=(
                    f"M{mag:.1f} | "
                    f"{severity} | "
                    f"{row['place']}"
                )
            ).add_to(fmap)

    # -------------------------------------------------------------------------
    # EARTHQUAKE HEATMAP
    # -------------------------------------------------------------------------

    if (
        show_heatmap
        and not india_eq.empty
        and len(india_eq) > 0
    ):

        heat_points = []

        for _, row in india_eq.iterrows():

            weight = max(
                0.2,
                min(1.0, row["magnitude"] / 7.0)
            )

            heat_points.append(
                [
                    row["latitude"],
                    row["longitude"],
                    weight
                ]
            )

        HeatMap(
            heat_points,
            radius=25,
            blur=18,
            min_opacity=0.25,
            max_zoom=7
        ).add_to(fmap)

    # -------------------------------------------------------------------------
    # WEATHER MARKERS
    # -------------------------------------------------------------------------

    if show_weather and not weather.empty:

        for _, row in weather.iterrows():

            risk = row["risk"]

            if risk == "HIGH":
                color = "#ff453a"
            elif risk == "MODERATE":
                color = "#ffcc00"
            else:
                color = "#32d74b"

            weather_text = weather_description(
                row["weather_code"]
            )

            popup_html = f"""
            <div style="font-family:Arial;min-width:220px;">
                <h4>WEATHER STATION</h4>
                <b>Location:</b> {row['city']}<br>
                <b>Temperature:</b> {row['temperature']} °C<br>
                <b>Humidity:</b> {row['humidity']} %<br>
                <b>Rain:</b> {row['rain']} mm<br>
                <b>Wind:</b> {row['wind_speed']} km/h<br>
                <b>Condition:</b> {weather_text}<br>
                <b>Risk:</b> {risk}<br>
            </div>
            """

            folium.CircleMarker(
                location=[
                    row["latitude"],
                    row["longitude"]
                ],
                radius=7,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.85,
                weight=2,
                popup=folium.Popup(
                    popup_html,
                    max_width=320
                ),
                tooltip=(
                    f"{row['city']} | "
                    f"{row['temperature']}°C | "
                    f"{risk}"
                )
            ).add_to(fmap)

    # -------------------------------------------------------------------------
    # LEGEND
    # -------------------------------------------------------------------------

    legend = """
    <div style="
        position: fixed;
        bottom: 25px;
        left: 25px;
        z-index: 9999;
        background: rgba(10,15,22,0.92);
        color: white;
        padding: 12px 15px;
        border-radius: 8px;
        border: 1px solid #344455;
        font-size: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.35);
    ">

    <b>EARTHSHIELD LEGEND</b><br><br>

    <span style="color:#ff3030;">●</span>
    Critical earthquake<br>

    <span style="color:#ff8a00;">●</span>
    High earthquake<br>

    <span style="color:#ffd60a;">●</span>
    Moderate / elevated<br>

    <span style="color:#36d399;">●</span>
    Low earthquake<br>

    <span style="color:#32d74b;">●</span>
    Weather normal<br>

    <span style="color:#ffcc00;">●</span>
    Weather moderate<br>

    <span style="color:#ff453a;">●</span>
    Weather high

    </div>
    """

    fmap.get_root().html.add_child(
        folium.Element(legend)
    )

    folium.LayerControl(
        collapsed=False
    ).add_to(fmap)

    return fmap


# =============================================================================
# COMMAND CENTER
# =============================================================================

if page == "Command Center":

    st.markdown(
        '<div class="section-title">NATIONAL SITUATIONAL AWARENESS</div>',
        unsafe_allow_html=True
    )

    eq_count = len(earthquakes)
    india_eq_count = len(india_eq)

    if not india_eq.empty:
        high_eq = int(
            (india_eq["magnitude"] >= 5.0).sum()
        )
    else:
        high_eq = 0

    if not weather.empty:
        weather_high = int(
            (weather["risk"] == "HIGH").sum()
        )
    else:
        weather_high = 0

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "GLOBAL EARTHQUAKES",
            eq_count,
            "last 24h"
        )

    with c2:
        st.metric(
            "INDIA REGION",
            india_eq_count,
            "events"
        )

    with c3:
        st.metric(
            "M5+ EVENTS",
            high_eq,
            "India region"
        )

    with c4:
        st.metric(
            "WEATHER STATIONS",
            len(weather),
            "monitored"
        )

    with c5:
        st.metric(
            "HIGH WEATHER",
            weather_high,
            "locations"
        )

    st.markdown(
        '<div class="section-title">LIVE GEOSPATIAL MONITOR</div>',
        unsafe_allow_html=True
    )

    fmap = create_map()

    map_result = st_folium(
        fmap,
        width=None,
        height=650,
        returned_objects=[
            "last_object_clicked",
            "last_object_clicked_popup"
        ]
    )

    # -------------------------------------------------------------------------
    # SELECTED MAP EVENT
    # -------------------------------------------------------------------------

    clicked = map_result.get(
        "last_object_clicked"
    )

    if clicked:

        st.markdown(
            '<div class="section-title">SELECTED MAP LOCATION</div>',
            unsafe_allow_html=True
        )

        st.json(clicked)

    # -------------------------------------------------------------------------
    # LOWER DASHBOARD
    # -------------------------------------------------------------------------

    left, right = st.columns([1.15, 0.85])

    with left:

        st.markdown(
            '<div class="section-title">RECENT INDIA-REGION EARTHQUAKES</div>',
            unsafe_allow_html=True
        )

        if india_eq.empty:

            st.info(
                "No earthquake events currently available "
                "inside the India monitoring zone."
            )

        else:

            display_eq = india_eq.copy()

            display_eq["UTC"] = display_eq["time"].apply(
                lambda x: (
                    x.strftime("%H:%M:%S")
                    if pd.notna(x)
                    else "-"
                )
            )

            display_eq = display_eq[
                [
                    "UTC",
                    "magnitude",
                    "severity",
                    "place",
                    "depth_km"
                ]
            ].head(12)

            display_eq.columns = [
                "Time",
                "Magnitude",
                "Severity",
                "Location",
                "Depth km"
            ]

            st.dataframe(
                display_eq,
                use_container_width=True,
                hide_index=True
            )

    with right:

        st.markdown(
            '<div class="section-title">WEATHER RISK BOARD</div>',
            unsafe_allow_html=True
        )

        if weather.empty:

            st.warning(
                "Weather service did not return data."
            )

        else:

            for _, row in weather.head(10).iterrows():

                symbol = severity_symbol(
                    "HIGH"
                    if row["risk"] == "HIGH"
                    else (
                        "MODERATE"
                        if row["risk"] == "MODERATE"
                        else "LOW"
                    )
                )

                st.markdown(
                    f"""
                    <div style="
                        background:#101824;
                        border:1px solid #263343;
                        border-radius:7px;
                        padding:8px;
                        margin-bottom:6px;
                    ">
                    {symbol}
                    <b>{row['city']}</b>
                    &nbsp; {row['temperature']}°C
                    &nbsp; | &nbsp; {weather_description(row['weather_code'])}
                    &nbsp; | &nbsp; {row['risk']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =============================================================================
# EARTHQUAKE MONITOR
# =============================================================================

elif page == "Earthquake Monitor":

    st.markdown(
        '<div class="section-title">EARTHQUAKE INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    if earthquakes.empty:

        st.error(
            "Earthquake data is currently unavailable."
        )

    else:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "24H EVENTS",
                len(earthquakes)
            )

        with col2:
            st.metric(
                "M5+",
                int(
                    (earthquakes["magnitude"] >= 5).sum()
                )
            )

        with col3:
            st.metric(
                "M6+",
                int(
                    (earthquakes["magnitude"] >= 6).sum()
                )
            )

        with col4:
            st.metric(
                "M7+",
                int(
                    (earthquakes["magnitude"] >= 7).sum()
                )
            )

        st.markdown(
            '<div class="section-title">GLOBAL EARTHQUAKE MAP</div>',
            unsafe_allow_html=True
        )

        eq_map = folium.Map(
            location=[20, 20],
            zoom_start=2,
            tiles=None
        )

        folium.TileLayer(
            "OpenStreetMap",
            name="Street"
        ).add_to(eq_map)

        folium.TileLayer(
            tiles=(
                "https://server.arcgisonline.com/ArcGIS/"
                "rest/services/World_Imagery/MapServer/tile/"
                "{z}/{y}/{x}"
            ),
            attr="Esri World Imagery",
            name="Satellite"
        ).add_to(eq_map)

        for _, row in earthquakes.iterrows():

            mag = row["magnitude"]

            if mag >= 7:
                color = "#ff3030"
            elif mag >= 6:
                color = "#ff8a00"
            elif mag >= 5:
                color = "#ffd60a"
            else:
                color = "#36d399"

            folium.CircleMarker(
                location=[
                    row["latitude"],
                    row["longitude"]
                ],
                radius=max(
                    3,
                    min(18, mag * 2)
                ),
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                tooltip=(
                    f"M{mag:.1f} | "
                    f"{row['place']}"
                )
            ).add_to(eq_map)

        folium.LayerControl().add_to(eq_map)

        st_folium(
            eq_map,
            width=None,
            height=620
        )

        st.markdown(
            '<div class="section-title">EARTHQUAKE EVENT TABLE</div>',
            unsafe_allow_html=True
        )

        table = earthquakes.copy()

        table["UTC"] = table["time"].apply(
            lambda x: (
                x.strftime("%Y-%m-%d %H:%M")
                if pd.notna(x)
                else "-"
            )
        )

        table = table[
            [
                "UTC",
                "magnitude",
                "place",
                "depth_km",
                "severity",
                "tsunami"
            ]
        ]

        table.columns = [
            "Time",
            "Magnitude",
            "Location",
            "Depth km",
            "Severity",
            "Tsunami"
        ]

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )


# =============================================================================
# WEATHER MONITOR
# =============================================================================

elif page == "Weather Monitor":

    st.markdown(
        '<div class="section-title">NATIONAL WEATHER MONITOR</div>',
        unsafe_allow_html=True
    )

    if weather.empty:

        st.error(
            "Weather data is currently unavailable."
        )

    else:

        high = int(
            (weather["risk"] == "HIGH").sum()
        )

        moderate = int(
            (weather["risk"] == "MODERATE").sum()
        )

        normal = int(
            (weather["risk"] == "LOW").sum()
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "HIGH RISK",
                high
            )

        with c2:
            st.metric(
                "MODERATE",
                moderate
            )

        with c3:
            st.metric(
                "LOW",
                normal
            )

        st.markdown(
            '<div class="section-title">WEATHER MAP</div>',
            unsafe_allow_html=True
        )

        weather_map = folium.Map(
            location=[22.5, 79],
            zoom_start=5,
            tiles=None
        )

        folium.TileLayer(
            "OpenStreetMap",
            name="Street"
        ).add_to(weather_map)

        folium.TileLayer(
            tiles=(
                "https://server.arcgisonline.com/ArcGIS/"
                "rest/services/World_Imagery/MapServer/tile/"
                "{z}/{y}/{x}"
            ),
            attr="Esri World Imagery",
            name="Satellite"
        ).add_to(weather_map)

        for _, row in weather.iterrows():

            if row["risk"] == "HIGH":
                color = "#ff453a"

            elif row["risk"] == "MODERATE":
                color = "#ffcc00"

            else:
                color = "#32d74b"

            popup = folium.Popup(
                f"""
                <b>{row['city']}</b><br>
                Temperature: {row['temperature']} °C<br>
                Humidity: {row['humidity']} %<br>
                Rain: {row['rain']} mm<br>
                Wind: {row['wind_speed']} km/h<br>
                Condition: {weather_description(row['weather_code'])}<br>
                Risk: {row['risk']}
                """,
                max_width=300
            )

            folium.CircleMarker(
                location=[
                    row["latitude"],
                    row["longitude"]
                ],
                radius=9,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.85,
                popup=popup,
                tooltip=row["city"]
            ).add_to(weather_map)

        folium.LayerControl().add_to(weather_map)

        st_folium(
            weather_map,
            width=None,
            height=620
        )

        st.markdown(
            '<div class="section-title">WEATHER STATION DATA</div>',
            unsafe_allow_html=True
        )

        weather_table = weather.copy()

        weather_table["Condition"] = weather_table[
            "weather_code"
        ].apply(weather_description)

        weather_table = weather_table[
            [
                "city",
                "temperature",
                "humidity",
                "rain",
                "wind_speed",
                "Condition",
                "risk"
            ]
        ]

        weather_table.columns = [
            "Location",
            "Temperature °C",
            "Humidity %",
            "Rain mm",
            "Wind km/h",
            "Condition",
            "Risk"
        ]

        st.dataframe(
            weather_table,
            use_container_width=True,
            hide_index=True
        )


# =============================================================================
# ALERT CENTER
# =============================================================================

elif page == "Alert Center":

    st.markdown(
        '<div class="section-title">ACTIVE DISASTER ALERT CENTER</div>',
        unsafe_allow_html=True
    )

    alerts = []

    if not india_eq.empty:

        for _, row in india_eq.iterrows():

            if row["magnitude"] >= 6:

                alerts.append(
                    {
                        "type": "EARTHQUAKE",
                        "severity": "CRITICAL"
                        if row["magnitude"] >= 7
                        else "HIGH",
                        "message": (
                            f"M{row['magnitude']:.1f} earthquake — "
                            f"{row['place']}"
                        )
                    }
                )

    if not weather.empty:

        for _, row in weather.iterrows():

            if row["risk"] == "HIGH":

                alerts.append(
                    {
                        "type": "WEATHER",
                        "severity": "HIGH",
                        "message": (
                            f"{row['city']} — "
                            f"{weather_description(row['weather_code'])}, "
                            f"{row['temperature']}°C, "
                            f"wind {row['wind_speed']} km/h"
                        )
                    }
                )

    if not alerts:

        st.markdown(
            """
            <div style="
                background:rgba(50,215,75,0.08);
                border:1px solid rgba(50,215,75,0.25);
                border-left:4px solid #32d74b;
                border-radius:8px;
                padding:18px;
            ">
            🟢 <b>NO HIGH-PRIORITY ALERTS DETECTED</b><br>
            <span style="color:#8fa3b8;">
            Monitoring systems remain active.
            </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        for alert in alerts:

            css_class = (
                "alert-critical"
                if alert["severity"] == "CRITICAL"
                else "alert-high"
            )

            symbol = (
                "🔴"
                if alert["severity"] == "CRITICAL"
                else "🟠"
            )

            st.markdown(
                f"""
                <div class="{css_class}">
                {symbol}
                <b>{alert['severity']} — {alert['type']}</b><br>
                {alert['message']}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="section-title">ALERT ENGINE STATUS</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "Earthquake Engine",
            "ONLINE"
        )

    with b:
        st.metric(
            "Weather Engine",
            "ONLINE"
        )

    with c:
        st.metric(
            "Geospatial Engine",
            "ONLINE"
        )


# =============================================================================
# SYSTEM STATUS
# =============================================================================

elif page == "System Status":

    st.markdown(
        '<div class="section-title">EARTHSHIELD SYSTEM STATUS</div>',
        unsafe_allow_html=True
    )

    components = [
        (
            "Streamlit Dashboard",
            "ONLINE"
        ),
        (
            "USGS Earthquake Feed",
            "ONLINE" if not earthquakes.empty else "OFFLINE"
        ),
        (
            "Open-Meteo Weather Feed",
            "ONLINE" if not weather.empty else "OFFLINE"
        ),
        (
            "Satellite Map Layer",
            "READY"
        ),
        (
            "Street Map Layer",
            "READY"
        ),
        (
            "Terrain Map Layer",
            "READY"
        ),
        (
            "India Monitoring Zone",
            "ACTIVE"
        ),
        (
            "Earthquake Heatmap",
            "ACTIVE"
        ),
        (
            "Day 2 Alert Engine",
            "AVAILABLE"
        ),
        (
            "Day 2 ENSO Monitor",
            "AVAILABLE"
        ),
    ]

    status_df = pd.DataFrame(
        components,
        columns=[
            "Component",
            "Status"
        ]
    )

    st.dataframe(
        status_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        '<div class="section-title">DATA PIPELINE</div>',
        unsafe_allow_html=True
    )

    st.code(
        """
LIVE SOURCES
│
├── USGS Earthquake GeoJSON
│       │
│       ├── Global earthquakes
│       ├── India-region filter
│       ├── Magnitude classification
│       └── Heatmap
│
├── Open-Meteo
│       │
│       ├── Temperature
│       ├── Rain
│       ├── Humidity
│       ├── Wind
│       └── Weather risk
│
└── Geospatial Layer
        │
        ├── Street
        ├── Satellite
        └── Terrain
        """,
        language="text"
    )

    st.markdown(
        '<div class="section-title">PROJECT STRUCTURE</div>',
        unsafe_allow_html=True
    )

    st.code(
        """
/content/EARTHSHIELD/

├── app/
│   ├── dashboard.py
│   ├── monitoring/
│   │   ├── national_weather.py
│   │   └── earthquake_monitor.py
│   ├── alerts/
│   │   └── alert_engine.py
│   └── climate/
│       └── enso_monitor.py
│
├── data/
│   └── processed/
│
└── DAY 3
    └── geospatial command center
        """,
        language="text"
    )


# =============================================================================
# FOOTER
# =============================================================================

st.markdown(
    """
<div class="footer">
EARTHSHIELD • Disaster Detection & Monitoring System<br>
DAY 3 — GEOSPATIAL COMMAND CENTER<br>
Live data should be interpreted with appropriate operational verification.
</div>
""",
    unsafe_allow_html=True
)


# =============================================================================
# AUTO REFRESH
# =============================================================================

if auto_refresh:

    time.sleep(refresh_seconds)
    st.rerun()
