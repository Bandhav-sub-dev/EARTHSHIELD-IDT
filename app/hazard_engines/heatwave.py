
from app.risk_engine import calculate_risk


def heatwave_risk(max_temperature_c):

    temperature = float(
        max_temperature_c
    )

    if temperature < 32:
        probability = 10
        severity = 15

    elif temperature < 36:
        probability = 30
        severity = 30

    elif temperature < 40:
        probability = 55
        severity = 55

    elif temperature < 45:
        probability = 75
        severity = 75

    else:
        probability = 90
        severity = 90

    return calculate_risk(
        hazard="Heatwave",
        probability=probability,
        severity=severity,
    )
