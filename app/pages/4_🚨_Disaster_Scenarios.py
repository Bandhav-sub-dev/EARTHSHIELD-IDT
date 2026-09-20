
import json
import math
from pathlib import Path

import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium


# =============================================================================
# EARTHSHIELD — MULTI-DISASTER SCENARIO SIMULATOR
# =============================================================================

st.set_page_config(
    page_title="EARTHSHIELD — Disaster Scenarios",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# STYLE
# =============================================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #07111f;
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] {
        background: #050b14;
    }

    .hero {
        background:
            linear-gradient(
                135deg,
                rgba(127,29,29,0.85),
                rgba(7,17,31,0.96)
            );
        border: 1px solid rgba(239,68,68,0.45);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 18px;
    }

    .hero h1 {
        margin: 0;
        color: white;
        font-size: 32px;
    }

    .hero p {
        color: #cbd5e1;
        margin-top: 7px;
    }

    .demo-warning {
        background: #21120a;
        border: 1px solid #f59e0b;
        color: #fde68a;
        padding: 12px 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }

    .sms {
        background: #061a12;
        border: 1px solid #22c55e;
        border-radius: 12px;
        padding: 16px;
        white-space: pre-wrap;
        font-family: monospace;
        color: #dcfce7;
    }

    .shelter {
        background: #071827;
        border: 1px solid #38bdf8;
        border-radius: 12px;
        padding: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


ROOT = Path("/content/EARTHSHIELD")
DEMO = ROOT / "data" / "demo"

PEOPLE_FILE = DEMO / "people_multi_area_demo.json"
FACILITY_FILE = DEMO / "facilities_multi_area_demo.json"
SCENARIO_FILE = DEMO / "multi_disaster_scenarios.json"


# =============================================================================
# LOAD DATA
# =============================================================================

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


people = load_json(PEOPLE_FILE)
facilities = load_json(FACILITY_FILE)
scenarios = load_json(SCENARIO_FILE)


# =============================================================================
# GEO FUNCTIONS
# =============================================================================

def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0

    p1 = math.radians(float(lat1))
    p2 = math.radians(float(lat2))

    dp = math.radians(float(lat2) - float(lat1))
    dl = math.radians(float(lon2) - float(lon1))

    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1)
        * math.cos(p2)
        * math.sin(dl / 2) ** 2
    )

    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def nearest_shelter(person, scenario):
    candidates = []

    for facility in facilities:

        if facility.get("status") != "OPEN":
            continue

        if facility.get("available_capacity", 0) <= 0:
            continue

        distance = haversine_km(
            person["latitude"],
            person["longitude"],
            facility["latitude"],
            facility["longitude"],
        )

        # Do not recommend a facility inside the simulated impact zone.
        shelter_to_disaster = haversine_km(
            scenario["latitude"],
            scenario["longitude"],
            facility["latitude"],
            facility["longitude"],
        )

        if shelter_to_disaster <= scenario["impact_radius_km"]:
            continue

        candidates.append(
            {
                "facility": facility,
                "distance": distance,
                "shelter_to_disaster": shelter_to_disaster,
            }
        )

    candidates.sort(key=lambda x: x["distance"])

    return candidates[0] if candidates else None


def get_affected_people(scenario):
    result = []

    for person in people:
        distance = haversine_km(
            scenario["latitude"],
            scenario["longitude"],
            person["latitude"],
            person["longitude"],
        )

        if distance <= scenario["impact_radius_km"]:
            result.append(
                {
                    "person": person,
                    "distance": distance,
                }
            )

    return sorted(result, key=lambda x: x["distance"])


def sms_text(person, scenario, shelter_info):
    shelter = shelter_info["facility"]

    return (
        "EARTHSHIELD DEMO ALERT\n"
        "--------------------------------\n"
        f"Hello {person['name']},\n\n"
        f"DISASTER: {scenario['disaster_type']}\n"
        f"SEVERITY: {scenario['severity']}\n"
        f"AREA: {scenario['area']}\n\n"
        "You are inside the simulated impact zone.\n\n"
        "NEAREST SAFE SHELTER\n"
        f"{shelter['name']}\n"
        f"{shelter['address']}\n"
        f"Distance: {shelter_info['distance']:.2f} km\n\n"
        "Available capacity: "
        f"{shelter['available_capacity']}\n\n"
        "Please follow official emergency instructions.\n\n"
        "[SIMULATION ONLY]\n"
        "This SMS was generated by EARTHSHIELD for demonstration.\n"
        "NO ACTUAL SMS HAS BEEN SENT."
    )


# =============================================================================
# HEADER
# =============================================================================

st.markdown(
    """
    <div class="hero">
        <h1>🚨 EARTHSHIELD — MULTI-DISASTER RESPONSE SIMULATOR</h1>
        <p>
        Simulate disaster impact → identify affected people →
        locate safe shelters → generate emergency SMS.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="demo-warning">
    ⚠️ <b>DEMO MODE:</b>
    All people, locations, shelters and phone numbers shown here are fictional.
    SMS messages are generated on screen only. No real SMS or emergency
    notification is sent.
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.header("SCENARIO CONTROL")

scenario_names = [
    f"{s['name']} — {s['disaster_type']}"
    for s in scenarios
]

selected_name = st.sidebar.selectbox(
    "Select disaster scenario",
    scenario_names,
)

selected_index = scenario_names.index(selected_name)
scenario = scenarios[selected_index]

st.sidebar.divider()

radius = st.sidebar.slider(
    "Impact radius (km)",
    min_value=1,
    max_value=50,
    value=int(scenario["impact_radius_km"]),
    step=1,
)

st.sidebar.divider()

st.sidebar.write("**Scenario Information**")
st.sidebar.write(f"Disaster: {scenario['disaster_type']}")
st.sidebar.write(f"Severity: {scenario['severity']}")
st.sidebar.write(f"Area: {scenario['area']}")


# =============================================================================
# SCENARIO HEADER
# =============================================================================

st.subheader(f"🚨 {scenario['name']}")

c1, c2, c3, c4 = st.columns(4)

affected = []

# Use selected slider radius instead of original scenario radius.
scenario_runtime = dict(scenario)
scenario_runtime["impact_radius_km"] = radius

affected = get_affected_people(scenario_runtime)

c1.metric("Disaster", scenario["disaster_type"])
c2.metric("Severity", scenario["severity"])
c3.metric("Impact Radius", f"{radius} km")
c4.metric("Affected Demo People", len(affected))


# =============================================================================
# MAP
# =============================================================================

st.markdown("### 🗺️ Disaster Impact Map")

m = folium.Map(
    location=[
        scenario["latitude"],
        scenario["longitude"],
    ],
    zoom_start=11,
    tiles="OpenStreetMap",
)

# Satellite layer
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/"
          "World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri World Imagery",
    name="Satellite",
    overlay=False,
    control=True,
).add_to(m)

# Disaster point
folium.Marker(
    [
        scenario["latitude"],
        scenario["longitude"],
    ],
    popup=(
        f"<b>{scenario['name']}</b><br>"
        f"{scenario['disaster_type']}<br>"
        f"Severity: {scenario['severity']}"
    ),
    tooltip="DISASTER EVENT",
    icon=folium.Icon(
        color="red",
        icon="warning-sign",
    ),
).add_to(m)

# Impact radius
folium.Circle(
    [
        scenario["latitude"],
        scenario["longitude"],
    ],
    radius=radius * 1000,
    color="#ef4444",
    fill=True,
    fill_opacity=0.12,
    popup=f"Simulated impact zone: {radius} km",
).add_to(m)


# Add all people
for entry in [
    {
        "person": p,
        "distance": haversine_km(
            scenario["latitude"],
            scenario["longitude"],
            p["latitude"],
            p["longitude"],
        ),
    }
    for p in people
]:

    person = entry["person"]
    distance = entry["distance"]

    inside = distance <= radius

    folium.CircleMarker(
        [
            person["latitude"],
            person["longitude"],
        ],
        radius=7 if inside else 5,
        color="#ef4444" if inside else "#38bdf8",
        fill=True,
        fill_opacity=0.9,
        popup=(
            f"<b>{person['name']}</b><br>"
            f"{person['city']}<br>"
            f"Distance: {distance:.2f} km<br>"
            f"Status: {'AFFECTED' if inside else 'SAFE'}"
        ),
    ).add_to(m)


# Add facilities
for facility in facilities:

    if facility["status"] != "OPEN":
        continue

    facility_distance = haversine_km(
        scenario["latitude"],
        scenario["longitude"],
        facility["latitude"],
        facility["longitude"],
    )

    # Do not visually hide shelters; show all.
    color = "green"

    folium.Marker(
        [
            facility["latitude"],
            facility["longitude"],
        ],
        popup=(
            f"<b>{facility['name']}</b><br>"
            f"{facility['type']}<br>"
            f"{facility['address']}<br>"
            f"Capacity: {facility['available_capacity']}"
        ),
        tooltip="EMERGENCY FACILITY",
        icon=folium.Icon(
            color=color,
            icon="home",
        ),
    ).add_to(m)

folium.LayerControl().add_to(m)

st_folium(
    m,
    width=None,
    height=600,
    returned_objects=[],
)


# =============================================================================
# AFFECTED PEOPLE
# =============================================================================

st.markdown("### 👥 Affected People")

if not affected:

    st.info(
        "No demo people are inside the selected impact radius."
    )

else:

    affected_rows = []

    for entry in affected:

        person = entry["person"]
        shelter = nearest_shelter(
            person,
            scenario_runtime,
        )

        affected_rows.append(
            {
                "Person": person["name"],
                "City": person["city"],
                "Distance": f"{entry['distance']:.2f} km",
                "Notification": (
                    "ENABLED"
                    if person["notification_enabled"]
                    else "DISABLED"
                ),
                "Nearest Shelter": (
                    shelter["facility"]["name"]
                    if shelter
                    else "NO SAFE SHELTER"
                ),
                "Shelter Distance": (
                    f"{shelter['distance']:.2f} km"
                    if shelter
                    else "N/A"
                ),
            }
        )

    st.dataframe(
        pd.DataFrame(affected_rows),
        use_container_width=True,
        hide_index=True,
    )


# =============================================================================
# PERSON RESPONSE
# =============================================================================

st.markdown("### 🧑‍🚒 Individual Emergency Response")

if affected:

    affected_people = [
        entry["person"]
        for entry in affected
    ]

    selected_person_name = st.selectbox(
        "Select affected person",
        [p["name"] for p in affected_people],
    )

    selected_person = next(
        p
        for p in affected_people
        if p["name"] == selected_person_name
    )

    shelter_info = nearest_shelter(
        selected_person,
        scenario_runtime,
    )

    left, right = st.columns(2)

    with left:

        st.markdown("#### 👤 Person")

        st.write(
            f"**Name:** {selected_person['name']}"
        )

        st.write(
            f"**Area:** {selected_person['city']}, "
            f"{selected_person['state']}"
        )

        st.write(
            f"**Location:** "
            f"{selected_person['latitude']:.5f}, "
            f"{selected_person['longitude']:.5f}"
        )

        st.write(
            f"**Demo phone:** {selected_person['mobile']}"
        )

        st.write(
            f"**Notification:** "
            f"{'Enabled' if selected_person['notification_enabled'] else 'Disabled'}"
        )

    with right:

        st.markdown("#### 🏠 Nearest Safe Shelter")

        if shelter_info:

            shelter = shelter_info["facility"]

            st.markdown(
                f"""
                <div class="shelter">
                <b>{shelter['name']}</b><br><br>
                📍 <b>Address:</b><br>
                {shelter['address']}<br><br>
                📏 <b>Distance:</b>
                {shelter_info['distance']:.2f} km<br><br>
                🏥 Medical:
                {'YES' if shelter['medical_support'] else 'NO'}<br>
                🍱 Food:
                {'YES' if shelter['food_available'] else 'NO'}<br>
                💧 Water:
                {'YES' if shelter['water_available'] else 'NO'}<br>
                ♿ Accessible:
                {'YES' if shelter['accessible'] else 'NO'}<br>
                👥 Available Capacity:
                {shelter['available_capacity']}
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.error(
                "No safe open shelter was found outside the simulated "
                "impact zone."
            )


# =============================================================================
# SMS SIMULATOR
# =============================================================================

st.markdown("### 📱 Emergency SMS Simulator")

st.caption(
    "Simulation only — this creates the message but does NOT send an SMS."
)

if affected:

    sms_person = st.selectbox(
        "Recipient",
        [p["name"] for p in affected_people],
        key="sms_recipient",
    )

    recipient = next(
        p
        for p in affected_people
        if p["name"] == sms_person
    )

    recipient_shelter = nearest_shelter(
        recipient,
        scenario_runtime,
    )

    if recipient_shelter:

        message = sms_text(
            recipient,
            scenario_runtime,
            recipient_shelter,
        )

        if st.button(
            "📱 GENERATE DEMO SMS",
            use_container_width=True,
        ):

            st.session_state["demo_sms"] = message
            st.session_state["sms_recipient"] = sms_person

            st.success(
                "Demo SMS generated. NO message was actually sent."
            )

        if "demo_sms" in st.session_state:

            st.markdown(
                f"""
                <div class="sms">{st.session_state["demo_sms"]}</div>
                """,
                unsafe_allow_html=True,
            )

            st.info(
                "📡 SMS gateway status: SIMULATED\n\n"
                "Provider: DEMO MODE\n\n"
                "Delivery status: NOT SENT"
            )

    else:

        st.warning(
            "No safe shelter available for this simulated recipient."
        )


# =============================================================================
# BATCH SMS SIMULATION
# =============================================================================

st.markdown("### 📡 Batch Notification Simulation")

if affected:

    if st.button(
        "🚨 SIMULATE ALERTING ALL AFFECTED PEOPLE",
        use_container_width=True,
    ):

        results = []

        for entry in affected:

            person = entry["person"]

            if not person["notification_enabled"]:
                results.append(
                    {
                        "Person": person["name"],
                        "Status": "SKIPPED",
                        "Reason": "Notifications disabled",
                    }
                )
                continue

            shelter = nearest_shelter(
                person,
                scenario_runtime,
            )

            if shelter:

                results.append(
                    {
                        "Person": person["name"],
                        "Status": "SIMULATED",
                        "Destination": person["mobile"],
                        "Shelter": shelter["facility"]["name"],
                        "Address": shelter["facility"]["address"],
                        "Distance": (
                            f"{shelter['distance']:.2f} km"
                        ),
                    }
                )

            else:

                results.append(
                    {
                        "Person": person["name"],
                        "Status": "NO SAFE SHELTER",
                        "Destination": person["mobile"],
                    }
                )

        st.session_state["batch_results"] = results

        st.success(
            f"Simulated notification processing complete for "
            f"{len(affected)} affected people."
        )

if "batch_results" in st.session_state:

    st.dataframe(
        pd.DataFrame(
            st.session_state["batch_results"]
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.warning(
        "DEMO ONLY: No real SMS, phone call, email, WhatsApp message, "
        "or emergency notification was transmitted."
    )


# =============================================================================
# DATASET INFORMATION
# =============================================================================

with st.expander("📦 Demo Dataset Information"):

    st.write(
        f"People: {len(people)} fictional records"
    )

    st.write(
        f"Emergency facilities: {len(facilities)} fictional records"
    )

    st.write(
        f"Disaster scenarios: {len(scenarios)} simulated scenarios"
    )

    st.write(
        "These datasets are intended for academic/prototype "
        "demonstration only."
    )
