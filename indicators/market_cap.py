from enum import StrEnum


class MarketCapCategory(StrEnum):
    LARGE = "LARGE"
    MID = "MID"
    SMALL = "SMALL"
    MICRO = "MICRO"


def market_cap_indicator(
    market_cap: float,
    tresholds={
        MarketCapCategory.LARGE: lambda c: c > 10_000_000_000,
        MarketCapCategory.MID: lambda c: c > 1_000_000_000,
        MarketCapCategory.SMALL: lambda c: c > 100_000_000,
        MarketCapCategory.MICRO: lambda c: c <= 100_000_000,
    },
) -> MarketCapCategory:
    return next(v for v, c in tresholds.items() if c(market_cap))
