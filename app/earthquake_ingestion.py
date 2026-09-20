
import requests
import pandas as pd

from app.utils.logger import info, error


USGS_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


def get_recent_earthquakes(min_magnitude=2.5, days=7):

    end = pd.Timestamp.utcnow()
    start = end - pd.Timedelta(days=days)

    params = {
        "format": "geojson",
        "starttime": start.isoformat(),
        "endtime": end.isoformat(),
        "minmagnitude": min_magnitude,
        "orderby": "time",
    }

    try:

        response = requests.get(
            USGS_URL,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        earthquakes = []

        for feature in data.get("features", []):

            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})

            coordinates = geometry.get(
                "coordinates",
                [None, None, None],
            )

            earthquakes.append({
                "id": feature.get("id"),
                "place": properties.get("place"),
                "magnitude": properties.get("mag"),
                "time": properties.get("time"),
                "longitude": coordinates[0],
                "latitude": coordinates[1],
                "depth_km": coordinates[2],
                "url": properties.get("url"),
            })

        info(
            f"Retrieved {len(earthquakes)} earthquake events"
        )

        return pd.DataFrame(earthquakes)

    except Exception as exc:

        error(
            f"Earthquake ingestion failed: {exc}"
        )

        return pd.DataFrame()
