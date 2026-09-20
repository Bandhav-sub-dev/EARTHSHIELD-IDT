
"""
EarthShield National Weather Monitor

Uses Open-Meteo for prototype national monitoring.

Important:
- Reference points represent state/UT monitoring locations.
- They are not complete geographic coverage.
- This module is an educational monitoring prototype.
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
import requests


PROJECT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = PROJECT / "config" / "india_monitoring_registry.json"

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def load_registry():
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)


def risk_level(score: float) -> str:
    if score >= 75:
        return "CRITICAL"
    if score >= 55:
        return "HIGH"
    if score >= 30:
        return "MODERATE"
    return "LOW"


def calculate_weather_risk(row) -> tuple[float, list[str]]:
    """
    Prototype weather risk score.

    This is NOT an official warning algorithm.
    """

    score = 0.0
    signals = []

    temperature = float(row.get("temperature_c", 0) or 0)
    precipitation = float(row.get("precipitation_mm", 0) or 0)
    wind = float(row.get("wind_kmh", 0) or 0)

    # Heat signal
    if temperature >= 45:
        score += 55
        signals.append("Extreme temperature")
    elif temperature >= 42:
        score += 40
        signals.append("Very high temperature")
    elif temperature >= 40:
        score += 25
        signals.append("High temperature")

    # Rain signal
    if precipitation >= 100:
        score += 50
        signals.append("Very heavy precipitation")
    elif precipitation >= 50:
        score += 35
        signals.append("Heavy precipitation")
    elif precipitation >= 25:
        score += 20
        signals.append("Elevated precipitation")

    # Wind signal
    if wind >= 90:
        score += 50
        signals.append("Very strong wind")
    elif wind >= 60:
        score += 35
        signals.append("Strong wind")
    elif wind >= 40:
        score += 15
        signals.append("Elevated wind")

    return min(score, 100), signals


def fetch_national_weather():
    registry = load_registry()

    names = list(registry.keys())
    lats = [registry[name]["lat"] for name in names]
    lons = [registry[name]["lon"] for name in names]

    params = {
        "latitude": ",".join(map(str, lats)),
        "longitude": ",".join(map(str, lons)),
        "current": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "surface_pressure",
            "weather_code",
        ]),
        "hourly": ",".join([
            "temperature_2m",
            "precipitation_probability",
            "precipitation",
            "wind_speed_10m",
        ]),
        "forecast_days": 2,
        "timezone": "Asia/Kolkata",
    }

    response = requests.get(
        OPEN_METEO_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    payload = response.json()

    # Open-Meteo returns a list when multiple locations are requested.
    if isinstance(payload, dict):
        payload = [payload]

    rows = []

    for index, item in enumerate(payload):
        name = names[index]
        current = item.get("current", {})

        row = {
            "region": name,
            "capital": registry[name]["capital"],
            "latitude": registry[name]["lat"],
            "longitude": registry[name]["lon"],
            "temperature_c": current.get("temperature_2m"),
            "humidity_pct": current.get("relative_humidity_2m"),
            "precipitation_mm": current.get("precipitation"),
            "wind_kmh": current.get("wind_speed_10m"),
            "pressure_hpa": current.get("surface_pressure"),
            "weather_code": current.get("weather_code"),
            "observed_at": current.get("time"),
            "source": "Open-Meteo",
        }

        score, signals = calculate_weather_risk(row)

        row["risk_score"] = round(score, 1)
        row["risk_level"] = risk_level(score)
        row["signals"] = "; ".join(signals) if signals else "No major prototype signal"

        rows.append(row)

    df = pd.DataFrame(rows)

    output = PROJECT / "data" / "processed" / "national_weather.csv"
    df.to_csv(output, index=False)

    return df
