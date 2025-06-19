from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class FNGData:
    value: float
    value_classification: str


class FNGSourcePort(ABC):
    @abstractmethod
    def get_fng(self) -> FNGData:
        pass
