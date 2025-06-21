from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from constants.asset import Asset


@dataclass(frozen=True)
class Market:
    name: str


class MarketsPort(ABC):
    @abstractmethod
    def get(self, asset: Asset) -> List[Market]:
        pass
