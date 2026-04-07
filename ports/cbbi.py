from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class CBBIData:
    value: int


class CBBISourcePort(ABC):
    @abstractmethod
    def get_cbbi(self) -> CBBIData:
        pass
