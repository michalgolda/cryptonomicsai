from constants.asset import Asset
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class GeneralAssetMetadata:
    name: str
    market_cap: float
    total_supply: float
    circulating_supply: float


class MarketDataPort(ABC):
    @abstractmethod
    def get_asset_metadata(self, asset: Asset) -> GeneralAssetMetadata:
        pass
