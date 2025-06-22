from abc import ABC, abstractmethod
from dataclasses import dataclass
from constants.asset import Asset


@dataclass(frozen=True)
class UrlsData:
    website_url: str
    white_paper_url: str


class UrlsPort(ABC):
    @abstractmethod
    def get(self, asset: Asset) -> UrlsData:
        pass
