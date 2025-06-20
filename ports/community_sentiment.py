from abc import ABC, abstractmethod
from dataclasses import dataclass

from constants.asset import Asset


@dataclass(frozen=True)
class CommunitySentimentData:
    bullish: int
    bearish: int


class CommunitySentimentPort(ABC):
    @abstractmethod
    def get(self, asset: Asset) -> CommunitySentimentData:
        pass
