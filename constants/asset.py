from enum import StrEnum


class Asset(StrEnum):
    BTC = "BTC"
    ETH = "ETH"
    TRX = "TRX"
    SUI = "SUI"


class AssetName(StrEnum):
    BTC = "bitcoin"
    ETH = "ethereum"
    TRX = "tron"
    SUI = "sui"
