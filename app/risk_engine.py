
from dataclasses import dataclass


@dataclass
class RiskResult:
    hazard: str
    score: float
    level: str
    explanation: str


def clamp(value, minimum=0, maximum=100):
    return max(
        minimum,
        min(maximum, float(value))
    )


def risk_level(score):

    score = clamp(score)

    if score <= 20:
        return "LOW"

    if score <= 40:
        return "MODERATE"

    if score <= 70:
        return "HIGH"

    if score <= 90:
        return "SEVERE"

    return "EXTREME"


def calculate_risk(
    hazard,
    probability,
    severity,
    exposure=1.0,
    vulnerability=1.0,
):

    probability = clamp(probability)
    severity = clamp(severity)

    exposure = max(
        0.0,
        float(exposure)
    )

    vulnerability = max(
        0.0,
        float(vulnerability)
    )

    score = (
        (probability / 100.0)
        * (severity / 100.0)
        * exposure
        * vulnerability
        * 100.0
    )

    score = clamp(score)

    level = risk_level(score)

    explanation = (
        f"{hazard}: "
        f"probability={probability:.1f}, "
        f"severity={severity:.1f}, "
        f"exposure={exposure:.2f}, "
        f"vulnerability={vulnerability:.2f}"
    )

    return RiskResult(
        hazard=hazard,
        score=round(score, 2),
        level=level,
        explanation=explanation,
    )
