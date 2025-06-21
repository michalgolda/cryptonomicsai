from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from constants.asset import Asset


@dataclass(frozen=True)
class Market:
    exchange_name: str
    volume24h: float


class TopMarketsPort(ABC):
    @abstractmethod
    def get(self, asset: Asset) -> List[Market]:
        pass
