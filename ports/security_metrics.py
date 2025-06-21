from typing import List
from abc import ABC, abstractmethod
from dataclasses import dataclass
from constants.asset import Asset


@dataclass(frozen=True)
class SecurityMetricData:
    name: str
    score: float


class SecurityMetricPort(ABC):
    @abstractmethod
    def get(self, asset: Asset) -> List[SecurityMetricData]:
        pass
