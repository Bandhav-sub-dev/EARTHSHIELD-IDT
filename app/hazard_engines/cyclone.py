
from app.risk_engine import calculate_risk


def cyclone_risk(
    wind_speed_kmh,
    probability=50,
):

    wind_speed_kmh = float(
        wind_speed_kmh
    )

    if wind_speed_kmh < 40:
        severity = 15

    elif wind_speed_kmh < 62:
        severity = 30

    elif wind_speed_kmh < 88:
        severity = 50

    elif wind_speed_kmh < 118:
        severity = 70

    elif wind_speed_kmh < 165:
        severity = 85

    else:
        severity = 95

    return calculate_risk(
        hazard="Cyclone",
        probability=probability,
        severity=severity,
    )
