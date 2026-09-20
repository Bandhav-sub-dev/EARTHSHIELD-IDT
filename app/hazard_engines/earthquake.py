
from app.risk_engine import calculate_risk


def earthquake_risk(magnitude):

    magnitude = float(magnitude)

    if magnitude < 3:
        probability = 20
        severity = 10

    elif magnitude < 4:
        probability = 35
        severity = 20

    elif magnitude < 5:
        probability = 50
        severity = 40

    elif magnitude < 6:
        probability = 70
        severity = 60

    elif magnitude < 7:
        probability = 85
        severity = 80

    else:
        probability = 95
        severity = 95

    return calculate_risk(
        hazard="Earthquake",
        probability=probability,
        severity=severity,
    )
