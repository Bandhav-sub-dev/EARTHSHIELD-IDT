
from app.risk_engine import calculate_risk


def rainfall_risk(
    precipitation_mm,
    duration_hours=1,
):

    precipitation_mm = float(
        precipitation_mm
    )

    duration_hours = max(
        float(duration_hours),
        1.0
    )

    rate = (
        precipitation_mm
        / duration_hours
    )

    if rate < 2:
        probability = 10
        severity = 15

    elif rate < 10:
        probability = 30
        severity = 30

    elif rate < 25:
        probability = 55
        severity = 50

    elif rate < 50:
        probability = 75
        severity = 70

    else:
        probability = 90
        severity = 90

    return calculate_risk(
        hazard="Rainfall",
        probability=probability,
        severity=severity,
    )
