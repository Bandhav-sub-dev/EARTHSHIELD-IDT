
import json
from pathlib import Path
import streamlit as st
import pandas as pd

PROJECT = Path(__file__).resolve().parents[2]
SOURCE_FILE = PROJECT / "data" / "source_registry.json"

st.set_page_config(
    page_title="EARTHSHIELD — Data Sources",
    page_icon="📡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #071019;
    color: #EAF2F8;
}

.source-card {
    border: 1px solid #29465D;
    background: #0C1824;
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("📡 EARTHSHIELD Data Sources")

st.info(
    "This page separates live external data sources from synthetic "
    "demonstration datasets used for system testing."
)

if SOURCE_FILE.exists():
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)
else:
    st.error(
        "EARTHSHIELD source registry was not found. "
        "Expected: data/source_registry.json"
    )
    registry = {
        "live_sources": [],
        "map_sources": [],
        "demo_sources": []
    }

st.metric(
    "Live source count",
    len(registry.get("live_sources", []))
)

st.metric(
    "Map source count",
    len(registry.get("map_sources", []))
)

st.metric(
    "Demo dataset count",
    len(registry.get("demo_sources", []))
)

st.subheader("🟢 Live Data Sources")

for source in registry.get("live_sources", []):

    st.markdown(
        f"""
        <div class="source-card">
        <h4>🟢 {source['name']}</h4>
        <b>Category:</b> {source['category']}<br>
        <b>Type:</b> {source['type']}<br>
        <b>URL:</b> {source.get('url', 'N/A')}<br>
        <b>Used for:</b> {', '.join(source.get('used_for', []))}
        </div>
        """,
        unsafe_allow_html=True
    )

st.subheader("🗺️ Map & Visualization Sources")

for source in registry.get("map_sources", []):

    st.markdown(
        f"""
        <div class="source-card">
        <h4>🗺️ {source['name']}</h4>
        <b>Category:</b> {source['category']}<br>
        <b>Type:</b> {source['type']}<br>
        <b>Purpose:</b> {source['used_for']}
        </div>
        """,
        unsafe_allow_html=True
    )

st.subheader("🟡 Synthetic Demonstration Datasets")

demo_rows = registry.get("demo_sources", [])

if demo_rows:
    demo_df = pd.DataFrame(demo_rows)
    st.dataframe(
        demo_df,
        use_container_width=True,
        hide_index=True
    )

st.warning(
    "Synthetic people and facility data are fictional and are intended "
    "only for software testing and academic demonstration."
)

st.subheader("🔬 Data Pipeline")

st.code("""
LIVE DATA
   ↓
DATA INGESTION
   ↓
VALIDATION
   ↓
NORMALIZATION
   ↓
DISASTER ANALYSIS
   ↓
IMPACT ZONE
   ↓
PEOPLE MATCHING
   ↓
ASSISTANCE RECOMMENDATION
   ↓
MAP + ALERTS + REPORT
""")

st.success("EARTHSHIELD data-source registry loaded successfully.")
