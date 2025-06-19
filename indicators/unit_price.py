from enum import StrEnum


class UnitPriceCategory(StrEnum):
    ULTRA_HIGH = "ULTRA_HIGH"
    VERY_HIGH = "VERY_HIGH"
    HIGH = "HIGH"
    UPPER_MID = "UPPER_MID"
    LOWER_MID = "LOWER_MID"
    LOW = "LOW"
    VERY_LOW = "VERY_LOW"


def unit_price_indicator(
    price: float,
    tresholds={
        UnitPriceCategory.ULTRA_HIGH: lambda p: p >= 10000,
        UnitPriceCategory.VERY_HIGH: lambda p: 1000 <= p < 10000,
        UnitPriceCategory.HIGH: lambda p: 100 <= p < 1000,
        UnitPriceCategory.UPPER_MID: lambda p: 10 <= p < 100,
        UnitPriceCategory.LOWER_MID: lambda p: 1 <= p < 10,
        UnitPriceCategory.LOW: lambda p: 0.01 <= p < 1,
        UnitPriceCategory.VERY_LOW: lambda p: p < 0.01,
    },
) -> UnitPriceCategory:
    return next(v for v, c in tresholds.items() if c(price))
