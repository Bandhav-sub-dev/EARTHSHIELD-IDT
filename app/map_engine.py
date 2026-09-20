
from pathlib import Path
import json
import math
import re
import requests
import folium
from folium.features import GeoJsonTooltip


ROOT = Path("/content/EARTHSHIELD")
GEOJSON_PATH = ROOT / "data" / "india_states.geojson"


def normalize_name(value):
    if value is None:
        return ""

    value = str(value).lower().strip()

    replacements = {
        "andaman & nicobar islands": "andaman and nicobar islands",
        "andaman and nicobar": "andaman and nicobar islands",
        "nct of delhi": "delhi",
        "new delhi": "delhi",
        "odisha": "odisha",
        "orissa": "odisha",
        "uttaranchal": "uttarakhand",
        "pondicherry": "puducherry",
        "jammu & kashmir": "jammu and kashmir",
        "jammu and kashmir": "jammu and kashmir",
        "tamilnadu": "tamil nadu",
        "chhattisgarh": "chhattisgarh",
    }

    value = re.sub(r"\s+", " ", value)
    return replacements.get(value, value)


def load_geojson():
    if not GEOJSON_PATH.exists():
        return None

    try:
        with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def extract_feature_name(feature):
    properties = feature.get("properties", {})

    preferred = [
        "NAME_1",
        "name",
        "NAME",
        "State",
        "STATE",
        "st_nm",
        "ST_NM",
        "state_name",
        "STATE_NAME",
    ]

    for key in preferred:
        if key in properties and properties[key]:
            return str(properties[key])

    for value in properties.values():
        if isinstance(value, str) and len(value) > 2:
            return value

    return "Unknown"


def create_risk_data(weather_df=None, earthquake_df=None):
    risk = {}

    if weather_df is not None and not weather_df.empty:
        for _, row in weather_df.iterrows():
            name = (
                row.get("state")
                or row.get("state_ut")
                or row.get("region")
                or row.get("name")
            )

            if not name:
                continue

            try:
                score = float(row.get("risk_score", 0))
            except Exception:
                score = 0.0

            risk[normalize_name(name)] = {
                "score": max(0.0, min(100.0, score)),
                "hazard": "Weather",
                "level": str(row.get("risk_level", "LOW")),
            }

    return risk


def risk_color(score):
    score = float(score)

    if score >= 75:
        return "#7f0000"
    if score >= 55:
        return "#d7301f"
    if score >= 30:
        return "#fc8d59"
    if score >= 15:
        return "#fed976"

    return "#31a354"


def create_intelligence_map(weather_df=None, earthquake_df=None):
    m = folium.Map(
        location=[22.5, 79.0],
        zoom_start=5,
        control_scale=True,
        tiles=None,
    )

    # Base maps
    folium.TileLayer(
        tiles="OpenStreetMap",
        name="🗺️ Standard Map",
        control=True,
        show=True,
    ).add_to(m)

    folium.TileLayer(
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ),
        attr="Esri World Imagery",
        name="🛰️ Satellite",
        overlay=False,
        control=True,
        show=False,
    ).add_to(m)

    folium.TileLayer(
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
        ),
        attr="Esri World Topographic Map",
        name="⛰️ Terrain",
        overlay=False,
        control=True,
        show=False,
    ).add_to(m)

    risk_data = create_risk_data(weather_df, earthquake_df)
    geojson = load_geojson()

    if geojson:
        def style_function(feature):
            feature_name = extract_feature_name(feature)
            record = risk_data.get(normalize_name(feature_name), {})
            score = record.get("score", 0)

            return {
                "fillColor": risk_color(score),
                "color": "#222222",
                "weight": 0.8,
                "fillOpacity": 0.62,
            }

        def highlight_function(feature):
            return {
                "weight": 2.5,
                "color": "#ffffff",
                "fillOpacity": 0.78,
            }

        tooltip_fields = []
        tooltip_aliases = []

        if geojson.get("features"):
            properties = geojson["features"][0].get("properties", {})

            name_key = None

            for candidate in [
                "NAME_1",
                "name",
                "NAME",
                "State",
                "STATE",
                "st_nm",
                "ST_NM",
                "state_name",
                "STATE_NAME",
            ]:
                if candidate in properties:
                    name_key = candidate
                    break

            if name_key:
                tooltip_fields.append(name_key)
                tooltip_aliases.append("State")

        if tooltip_fields:
            tooltip = GeoJsonTooltip(
                fields=tooltip_fields,
                aliases=tooltip_aliases,
                localize=True,
                sticky=True,
                labels=True,
            )
        else:
            tooltip = None

        layer = folium.GeoJson(
            geojson,
            name="🇮🇳 India State Risk",
            style_function=style_function,
            highlight_function=highlight_function,
            tooltip=tooltip,
            show=True,
        )

        layer.add_to(m)

    # Earthquake markers
    if earthquake_df is not None and not earthquake_df.empty:
        quake_group = folium.FeatureGroup(
            name="🌎 Earthquakes",
            show=True,
        )

        for _, row in earthquake_df.iterrows():
            try:
                lat = float(row.get("latitude"))
                lon = float(row.get("longitude"))
                mag = float(row.get("magnitude", 0))
            except Exception:
                continue

            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                continue

            if mag >= 6.5:
                color = "darkred"
            elif mag >= 5.5:
                color = "red"
            elif mag >= 4.5:
                color = "orange"
            else:
                color = "blue"

            popup_text = (
                f"<b>Earthquake</b><br>"
                f"Magnitude: {mag:.1f}<br>"
                f"Latitude: {lat:.2f}<br>"
                f"Longitude: {lon:.2f}"
            )

            folium.CircleMarker(
                location=[lat, lon],
                radius=max(4, min(12, mag * 1.5)),
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.75,
                popup=folium.Popup(popup_text, max_width=260),
            ).add_to(quake_group)

        quake_group.add_to(m)

    folium.LayerControl(
        collapsed=False,
        position="topright",
    ).add_to(m)

    return m


def create_satellite_map():
    m = folium.Map(
        location=[22.5, 79.0],
        zoom_start=5,
        control_scale=True,
        tiles=None,
    )

    folium.TileLayer(
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ),
        attr="Esri World Imagery",
        name="🛰️ Satellite Imagery",
        overlay=False,
        show=True,
    ).add_to(m)

    folium.TileLayer(
        tiles="OpenStreetMap",
        name="🗺️ Street Map",
        overlay=False,
        show=False,
    ).add_to(m)

    folium.TileLayer(
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
        ),
        attr="Esri World Topographic Map",
        name="⛰️ Terrain",
        overlay=False,
        show=False,
    ).add_to(m)

    # India boundary
    geojson = load_geojson()

    if geojson:
        folium.GeoJson(
            geojson,
            name="🇮🇳 India State Boundaries",
            style_function=lambda feature: {
                "fillColor": "transparent",
                "color": "#ffffff",
                "weight": 1.0,
                "fillOpacity": 0.0,
            },
            show=True,
        ).add_to(m)

    folium.LayerControl(
        collapsed=False,
        position="topright",
    ).add_to(m)

    return m
