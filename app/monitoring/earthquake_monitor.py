
"""
EarthShield India Earthquake Monitor

USGS FDSN GeoJSON feed.
Monitoring box is approximately India and surrounding region.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
import requests


PROJECT = Path(__file__).resolve().parents[2]

USGS_URL = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query"
)


def fetch_india_earthquakes(
    min_magnitude: float = 2.5,
    days: int = 7,
):
    now = datetime.now(timezone.utc)
    start = now - pd.Timedelta(days=days)

    params = {
        "format": "geojson",
        "starttime": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "endtime": now.strftime("%Y-%m-%dT%H:%M:%S"),
        "minlatitude": 5,
        "maxlatitude": 38,
        "minlongitude": 65,
        "maxlongitude": 100,
        "minmagnitude": min_magnitude,
        "orderby": "time",
    }

    response = requests.get(
        USGS_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    payload = response.json()

    rows = []

    for feature in payload.get("features", []):
        props = feature.get("properties", {})
        geometry = feature.get("geometry", {})

        coordinates = geometry.get("coordinates", [None, None, None])

        magnitude = props.get("mag")

        if magnitude is None:
            continue

        if magnitude >= 6.5:
            level = "CRITICAL"
        elif magnitude >= 5.5:
            level = "HIGH"
        elif magnitude >= 4.5:
            level = "MODERATE"
        else:
            level = "LOW"

        rows.append({
            "time": pd.to_datetime(
                props.get("time"),
                unit="ms",
                utc=True,
            ),
            "magnitude": magnitude,
            "place": props.get("place"),
            "latitude": coordinates[1],
            "longitude": coordinates[0],
            "depth_km": coordinates[2],
            "risk_level": level,
            "source": "USGS",
            "url": props.get("url"),
        })

    df = pd.DataFrame(rows)

    if not df.empty:
        df = df.sort_values("time", ascending=False)

    output = PROJECT / "data" / "processed" / "india_earthquakes.csv"
    df.to_csv(output, index=False)

    return df
