from enum import StrEnum


class Asset(StrEnum):
    BTC = "BTC"
    ETH = "ETH"
    TRX = "TRX"
    SUI = "SUI"
    BEAM = "BEAM"


class AssetName(StrEnum):
    BTC = "bitcoin"
    ETH = "ethereum"
    TRX = "tron"
    SUI = "sui"
    BEAM = "beam"
