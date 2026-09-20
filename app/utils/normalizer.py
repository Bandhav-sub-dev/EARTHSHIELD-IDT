
from datetime import datetime, timezone


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def normalize_location(name, latitude, longitude):
    return {
        "name": name,
        "latitude": float(latitude),
        "longitude": float(longitude),
    }


def normalize_hazard(
    hazard_type,
    value=None,
    probability=None,
    severity=None,
    latitude=None,
    longitude=None,
    source=None,
    timestamp=None,
    metadata=None,
):
    return {
        "hazard_type": hazard_type,
        "value": value,
        "probability": probability,
        "severity": severity,
        "latitude": latitude,
        "longitude": longitude,
        "source": source,
        "timestamp": timestamp or utc_now(),
        "metadata": metadata or {},
    }
