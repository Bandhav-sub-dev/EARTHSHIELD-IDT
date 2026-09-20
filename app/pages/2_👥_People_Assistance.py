
import json
import math
from pathlib import Path

import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

PROJECT = Path("/content/EARTHSHIELD")
DEMO_DIR = PROJECT / "data" / "demo"

PEOPLE_FILE = DEMO_DIR / "people_demo.json"
FACILITIES_FILE = DEMO_DIR / "emergency_facilities_demo.json"
SCENARIOS_FILE = DEMO_DIR / "disaster_test_scenarios.json"


st.set_page_config(
    page_title="EARTHSHIELD — People Assistance",
    page_icon="👥",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #071019;
    color: #EAF2F8;
}

[data-testid="stSidebar"] {
    background: #0A141F;
}

h1, h2, h3 {
    color: #EAF2F8;
}

.demo-banner {
    padding: 12px 16px;
    border: 1px solid #36566F;
    border-radius: 10px;
    background: #0C1A27;
    margin-bottom: 18px;
}

.metric-box {
    padding: 15px;
    border: 1px solid #29465D;
    border-radius: 10px;
    background: #0C1824;
    text-align: center;
}

.alert-box {
    padding: 12px;
    border-left: 4px solid #E74C3C;
    border-radius: 6px;
    background: #241316;
    margin: 6px 0;
}
</style>
""", unsafe_allow_html=True)


def load_json(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


people = load_json(PEOPLE_FILE)
facilities = load_json(FACILITIES_FILE)
scenarios = load_json(SCENARIOS_FILE)

people_df = pd.DataFrame(people)
facilities_df = pd.DataFrame(facilities)
scenarios_df = pd.DataFrame(scenarios)


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0

    p1 = math.radians(float(lat1))
    p2 = math.radians(float(lat2))

    dp = math.radians(float(lat2) - float(lat1))
    dl = math.radians(float(lon2) - float(lon1))

    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    )

    return 2 * R * math.asin(math.sqrt(a))


def find_affected_people(event_lat, event_lon, radius_km):
    result = []

    for person in people:
        distance = haversine_km(
            event_lat,
            event_lon,
            person["latitude"],
            person["longitude"]
        )

        row = dict(person)
        row["distance_km"] = round(distance, 2)
        row["affected"] = distance <= radius_km

        if row["affected"]:
            result.append(row)

    return result


def find_nearby_facilities(
    person_lat,
    person_lon,
    disaster_type,
    max_distance_km=30
):
    result = []

    for facility in facilities:
        if str(facility.get("status", "")).upper() != "OPEN":
            continue

        available = (
            int(facility.get("capacity", 0))
            - int(facility.get("current_occupancy", 0))
        )

        if available <= 0:
            continue

        distance = haversine_km(
            person_lat,
            person_lon,
            facility["latitude"],
            facility["longitude"]
        )

        if distance > max_distance_km:
            continue

        facility_type = str(facility.get("type", "")).lower()

        if disaster_type.lower() in ["earthquake", "flood", "cyclone", "wildfire"]:
            if facility_type not in [
                "shelter",
                "hospital",
                "relief center",
                "fire station"
            ]:
                continue

        row = dict(facility)
        row["available_capacity"] = available
        row["distance_km"] = round(distance, 2)

        result.append(row)

    result.sort(key=lambda x: x["distance_km"])

    return result


st.title("👥 People Safety & Emergency Assistance")

st.markdown("""
<div class="demo-banner">
<b>🟡 SYNTHETIC DEMONSTRATION MODE</b><br>
All people, facilities and disaster scenarios shown on this page are
fictional test data created for EARTHSHIELD system validation.
They do not represent real people or real emergency incidents.
</div>
""", unsafe_allow_html=True)


# -------------------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------------------

st.sidebar.header("🎛️ Demo Controls")

scenario_names = [
    s["name"]
    for s in scenarios
]

selected_name = st.sidebar.selectbox(
    "Select disaster test scenario",
    scenario_names
)

selected = next(
    s for s in scenarios
    if s["name"] == selected_name
)

radius = st.sidebar.slider(
    "Impact radius (km)",
    min_value=1,
    max_value=50,
    value=int(selected["impact_radius_km"]),
    step=1
)

run_demo = st.sidebar.button(
    "🚨 RUN DISASTER SCENARIO",
    use_container_width=True
)


# -------------------------------------------------------------------------
# TOP METRICS
# -------------------------------------------------------------------------

affected = find_affected_people(
    selected["latitude"],
    selected["longitude"],
    radius
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Demo People", len(people))

with col2:
    st.metric("Affected People", len(affected))

with col3:
    st.metric("Emergency Facilities", len(facilities))

with col4:
    st.metric("Severity", selected["severity"])


# -------------------------------------------------------------------------
# SCENARIO INFORMATION
# -------------------------------------------------------------------------

st.subheader("🚨 Active Test Scenario")

scenario_col1, scenario_col2 = st.columns(2)

with scenario_col1:
    st.write(f"**Scenario:** {selected['name']}")
    st.write(f"**Disaster:** {selected['type']}")
    st.write(f"**Severity:** {selected['severity']}")
    st.write(f"**Impact Radius:** {radius} km")

with scenario_col2:
    st.write(f"**Latitude:** {selected['latitude']}")
    st.write(f"**Longitude:** {selected['longitude']}")
    st.write(f"**Scenario ID:** {selected['scenario_id']}")
    st.write(f"**Description:** {selected['description']}")


# -------------------------------------------------------------------------
# MAP
# -------------------------------------------------------------------------

st.subheader("🗺️ People + Disaster + Emergency Facilities")

m = folium.Map(
    location=[
        selected["latitude"],
        selected["longitude"]
    ],
    zoom_start=11,
    tiles="OpenStreetMap"
)

# Disaster location
folium.Marker(
    [
        selected["latitude"],
        selected["longitude"]
    ],
    tooltip=f"🚨 {selected['type']} — {selected['severity']}",
    popup=(
        f"<b>DEMO DISASTER</b><br>"
        f"Type: {selected['type']}<br>"
        f"Severity: {selected['severity']}<br>"
        f"Impact radius: {radius} km"
    ),
    icon=folium.Icon(
        color="red",
        icon="warning-sign"
    )
).add_to(m)

# Impact radius
folium.Circle(
    [
        selected["latitude"],
        selected["longitude"]
    ],
    radius=radius * 1000,
    color="red",
    fill=True,
    fill_opacity=0.10,
    tooltip=f"Impact radius: {radius} km"
).add_to(m)

# People
for person in people:
    is_affected = person["person_id"] in {
        p["person_id"] for p in affected
    }

    color = "red" if is_affected else "green"

    folium.CircleMarker(
        [
            person["latitude"],
            person["longitude"]
        ],
        radius=7,
        color=color,
        fill=True,
        fill_opacity=0.85,
        tooltip=(
            f"{person['person_id']} — "
            f"{'AFFECTED' if is_affected else 'SAFE'}"
        ),
        popup=(
            f"<b>{person['name']}</b><br>"
            f"ID: {person['person_id']}<br>"
            f"City: {person['city']}<br>"
            f"Mobility: {person['mobility_status']}<br>"
            f"Status: {'AFFECTED' if is_affected else 'SAFE'}"
        )
    ).add_to(m)

# Facilities
facility_icons = {
    "Shelter": "home",
    "Hospital": "plus",
    "Fire Station": "fire",
    "Relief Center": "cutlery",
    "Water Center": "tint"
}

for facility in facilities:

    available = (
        int(facility["capacity"])
        - int(facility["current_occupancy"])
    )

    icon_name = facility_icons.get(
        facility["type"],
        "info-sign"
    )

    folium.Marker(
        [
            facility["latitude"],
            facility["longitude"]
        ],
        tooltip=(
            f"🏥 {facility['name']} "
            f"({available} spaces)"
        ),
        popup=(
            f"<b>{facility['name']}</b><br>"
            f"Type: {facility['type']}<br>"
            f"Available Capacity: {available}<br>"
            f"Medical: {facility['medical_support']}<br>"
            f"Food: {facility['food_available']}<br>"
            f"Water: {facility['water_available']}<br>"
            f"Status: {facility['status']}"
        ),
        icon=folium.Icon(
            color="blue",
            icon=icon_name
        )
    ).add_to(m)

st_folium(
    m,
    width=None,
    height=620,
    returned_objects=[]
)


# -------------------------------------------------------------------------
# AFFECTED PEOPLE
# -------------------------------------------------------------------------

st.subheader("🚨 People Requiring Attention")

if affected:

    alert_df = pd.DataFrame(affected)

    display_columns = [
        "person_id",
        "name",
        "city",
        "district",
        "mobility_status",
        "preferred_language",
        "distance_km",
        "notification_enabled"
    ]

    st.dataframe(
        alert_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    st.info(
        f"EARTHSHIELD identified {len(affected)} synthetic demo people "
        f"inside the {radius} km test impact zone."
    )

else:
    st.success(
        "No demo people are currently inside the selected impact zone."
    )


# -------------------------------------------------------------------------
# ASSISTANCE RECOMMENDATIONS
# -------------------------------------------------------------------------

st.subheader("🏥 Emergency Assistance Recommendations")

if affected:

    selected_person_id = st.selectbox(
        "Select an affected demo person",
        [
            p["person_id"]
            for p in affected
        ]
    )

    person = next(
        p for p in affected
        if p["person_id"] == selected_person_id
    )

    nearby = find_nearby_facilities(
        person["latitude"],
        person["longitude"],
        selected["type"]
    )

    if nearby:

        rec_df = pd.DataFrame(nearby)

        display_columns = [
            "facility_id",
            "name",
            "type",
            "distance_km",
            "available_capacity",
            "medical_support",
            "food_available",
            "water_available",
            "accessible"
        ]

        st.dataframe(
            rec_df[display_columns],
            use_container_width=True,
            hide_index=True
        )

        best = nearby[0]

        st.success(
            f"Nearest suitable open facility in this demo: "
            f"{best['name']} — {best['distance_km']} km away."
        )

    else:
        st.warning(
            "No suitable open demo facility was found within the search range."
        )


# -------------------------------------------------------------------------
# SIMULATED ALERT
# -------------------------------------------------------------------------

st.subheader("📢 Simulated Notification")

if run_demo:

    if affected:

        st.warning(
            f"🚨 DEMO ALERT GENERATED — "
            f"{len(affected)} synthetic people identified "
            f"inside the disaster impact zone."
        )

        for person in affected[:8]:

            st.markdown(
                f"""
                <div class="alert-box">
                <b>DEMO ALERT → {person['person_id']}</b><br>
                Disaster: {selected['type']}<br>
                Severity: {selected['severity']}<br>
                Distance from event: {person['distance_km']} km<br>
                Notification enabled: {person['notification_enabled']}<br>
                <b>Action:</b> Move toward an appropriate emergency facility
                and follow official emergency instructions.
                </div>
                """,
                unsafe_allow_html=True
            )

        if len(affected) > 8:
            st.info(
                f"{len(affected) - 8} additional demo alerts generated."
            )

    else:
        st.success(
            "Scenario executed successfully. "
            "No demo people were inside the selected impact zone."
        )

else:
    st.caption(
        "Press RUN DISASTER SCENARIO to execute the synthetic test."
    )


# -------------------------------------------------------------------------
# DATASET PREVIEW
# -------------------------------------------------------------------------

with st.expander("📊 View Synthetic People Dataset"):
    st.dataframe(
        people_df,
        use_container_width=True,
        hide_index=True
    )

with st.expander("🏥 View Emergency Facility Dataset"):
    st.dataframe(
        facilities_df,
        use_container_width=True,
        hide_index=True
    )

with st.expander("🧪 View Test Scenarios"):
    st.dataframe(
        scenarios_df,
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "EARTHSHIELD Day 3.5 — synthetic demonstration environment. "
    "Real-world emergency decisions should rely on verified official authorities."
)
