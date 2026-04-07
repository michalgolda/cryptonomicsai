from enum import StrEnum


class MarketCapClassification(StrEnum):
    LARGE = "LARGE"
    MID = "MID"
    SMALL = "SMALL"
    MICRO = "MICRO"


def market_cap_indicator(
    market_cap: float,
    tresholds={
        MarketCapClassification.LARGE: lambda c: c > 10_000_000_000,
        MarketCapClassification.MID: lambda c: c > 1_000_000_000,
        MarketCapClassification.SMALL: lambda c: c > 100_000_000,
        MarketCapClassification.MICRO: lambda c: c <= 100_000_000,
    },
) -> MarketCapClassification:
    return next(v for v, c in tresholds.items() if c(market_cap))
