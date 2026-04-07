from enum import StrEnum


class FNGClassification(StrEnum):
    EXTREME_FEAR = "EXTREME_FEAR"
    FEAR = "FEAR"
    NEUTRAL = "NEUTRAL"
    GREED = "GREED"
    EXTREME_GREED = "EXTREME_GREED"


def fng_indicator(
    value: float,
    thresholds={
        FNGClassification.EXTREME_FEAR: lambda v: v < 25,
        FNGClassification.FEAR: lambda v: v < 45,
        FNGClassification.NEUTRAL: lambda v: v < 55,
        FNGClassification.GREED: lambda v: v < 75,
        FNGClassification.EXTREME_GREED: lambda v: v >= 75,
    },
) -> FNGClassification:
    return next(c for c, check in thresholds.items() if check(value))
