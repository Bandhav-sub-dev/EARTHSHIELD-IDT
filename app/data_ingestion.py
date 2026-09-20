
import requests
import pandas as pd

from app.utils.logger import info, error


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(latitude, longitude, forecast_days=7):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "rain",
            "wind_speed_10m",
            "wind_gusts_10m",
        ]),
        "daily": ",".join([
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "rain_sum",
            "wind_speed_10m_max",
        ]),
        "forecast_days": forecast_days,
        "timezone": "auto",
    }

    try:
        response = requests.get(
            OPEN_METEO_URL,
            params=params,
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        info(
            f"Weather data received for "
            f"{latitude}, {longitude}"
        )

        return data

    except Exception as exc:
        error(f"Weather ingestion failed: {exc}")
        return None


def weather_to_dataframe(data):
    if not data or "hourly" not in data:
        return pd.DataFrame()

    return pd.DataFrame(data["hourly"])


def daily_to_dataframe(data):
    if not data or "daily" not in data:
        return pd.DataFrame()

    return pd.DataFrame(data["daily"])
