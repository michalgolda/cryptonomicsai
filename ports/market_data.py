from enum import StrEnum
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Asset(StrEnum):
    BTC = "BTC"
    ETH = "ETH"


@dataclass(frozen=True)
class GeneralAssetMetadata:
    name: str
    total_supply: float
    circulating_supply: float


class MarketDataPort(ABC):
    @abstractmethod
    def get_asset_metadata(self, asset: Asset) -> GeneralAssetMetadata:
        pass
