from enum import StrEnum


class CBBIClassification(StrEnum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"


def cbbi_indicator(value: int) -> CBBIClassification:
    return CBBIClassification.BULLISH if value <= 10 else CBBIClassification.BEARISH
