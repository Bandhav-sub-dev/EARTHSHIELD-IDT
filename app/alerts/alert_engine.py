
"""
EarthShield National Alert Engine.

Alerts are generated from prototype thresholds.
They are NOT official disaster warnings.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json

import pandas as pd


PROJECT = Path(__file__).resolve().parents[2]


def generate_weather_alerts(weather_df: pd.DataFrame):
    alerts = []

    if weather_df is None or weather_df.empty:
        return alerts

    for _, row in weather_df.iterrows():

        score = float(row.get("risk_score", 0) or 0)

        if score < 30:
            continue

        level = row.get("risk_level", "LOW")
        signals = row.get("signals", "")

        alerts.append({
            "hazard": "Weather",
            "region": row["region"],
            "level": level,
            "score": round(score, 1),
            "message": signals,
            "source": "Open-Meteo",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "MONITORING",
        })

    return alerts


def generate_earthquake_alerts(eq_df: pd.DataFrame):
    alerts = []

    if eq_df is None or eq_df.empty:
        return alerts

    for _, row in eq_df.iterrows():

        magnitude = float(row.get("magnitude", 0) or 0)

        # Prototype monitoring threshold.
        if magnitude < 4.5:
            continue

        alerts.append({
            "hazard": "Earthquake",
            "region": row.get("place", "Unknown"),
            "level": row.get("risk_level", "MODERATE"),
            "score": min(100, magnitude * 15),
            "message": f"Magnitude {magnitude:.1f} earthquake detected",
            "source": "USGS",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "MONITORING",
        })

    return alerts


def build_alerts(weather_df, eq_df):

    alerts = []

    alerts.extend(
        generate_weather_alerts(weather_df)
    )

    alerts.extend(
        generate_earthquake_alerts(eq_df)
    )

    alerts.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    output = PROJECT / "data" / "processed" / "active_alerts.json"

    with open(output, "w") as f:
        json.dump(alerts, f, indent=2)

    return alerts
