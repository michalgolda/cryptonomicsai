from enum import StrEnum
from typing import Dict, Callable


class DilutionRiskClassification(StrEnum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


def dilution_risk_indicator(
    total_supply: float,
    circulating_supply: float,
    thresholds: Dict[DilutionRiskClassification, Callable[[float], bool]] = {
        DilutionRiskClassification.VERY_LOW: lambda r: r >= 0.92,
        DilutionRiskClassification.LOW: lambda r: 0.85 <= r < 0.92,
        DilutionRiskClassification.MEDIUM: lambda r: 0.60 <= r < 0.85,
        DilutionRiskClassification.HIGH: lambda r: 0.30 <= r < 0.60,
        DilutionRiskClassification.VERY_HIGH: lambda r: r < 0.30,
    },
) -> DilutionRiskClassification:
    circulating_supply_ratio = round(circulating_supply / total_supply, 2)
    return next(v for v, c in thresholds.items() if c(circulating_supply_ratio))
