
"""
EarthShield ENSO Monitor.

Downloads NOAA CPC ONI data and classifies the latest published
three-month running oceanic Niño index.

This is a climate monitoring indicator, NOT a disaster prediction model.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import re

import pandas as pd
import requests


PROJECT = Path(__file__).resolve().parents[2]

# NOAA CPC operational ONI text data.
NOAA_ONI_URL = (
    "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
)


def classify_enso(oni_value: float):

    if oni_value >= 0.5:
        return "El Niño"

    if oni_value <= -0.5:
        return "La Niña"

    return "Neutral"


def fetch_enso():

    response = requests.get(
        NOAA_ONI_URL,
        timeout=30,
    )

    response.raise_for_status()

    text = response.text

    rows = []

    # NOAA table commonly contains:
    # SEAS YEAR TOTAL ANOM
    #
    # We primarily need the latest numeric anomaly.
    for line in text.splitlines():

        parts = line.strip().split()

        if len(parts) < 4:
            continue

        try:
            season = parts[0]
            year = int(parts[1])
            total = float(parts[2])
            anomaly = float(parts[3])
        except Exception:
            continue

        rows.append({
            "season": season,
            "year": year,
            "total": total,
            "oni": anomaly,
        })

    if not rows:
        raise RuntimeError(
            "NOAA ONI data could not be parsed."
        )

    df = pd.DataFrame(rows)

    latest = df.iloc[-1]

    oni = float(latest["oni"])

    state = classify_enso(oni)

    result = {
        "season": str(latest["season"]),
        "year": int(latest["year"]),
        "oni": oni,
        "state": state,
        "source": "NOAA CPC",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "interpretation": (
            "Warm ENSO indicator"
            if state == "El Niño"
            else
            "Cool ENSO indicator"
            if state == "La Niña"
            else
            "ENSO-neutral indicator"
        ),
    }

    output = PROJECT / "data" / "processed" / "enso_status.json"

    import json

    with open(output, "w") as f:
        json.dump(result, f, indent=2)

    df.to_csv(
        PROJECT / "data" / "processed" / "enso_history.csv",
        index=False,
    )

    return result, df
