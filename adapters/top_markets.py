import requests
from constants.asset import Asset, AssetName
from ports.top_markets import TopMarketsPort, Market
from typing import List, override
from logger import get_logger

logger = get_logger(__name__)


class DropsTabTopMarketsAdapter(TopMarketsPort):
    def __get_asset_name(self, asset: Asset) -> str:
        return AssetName[asset.value].value

    @override
    def get(self, asset: Asset) -> List[Market]:
        logger.info("Fetching top markets for %s from DropsTab", asset.value)
        asset_name = self.__get_asset_name(asset)
        res = requests.get(
            f"https://api2.icodrops.com/portfolio/api/exchange/{asset_name}/topMarkets"
        )
        res = res.json()

        return [
            Market(exchange_name=m.get("exchangeName"), volume24h=m.get("volume24h"))
            for m in res
        ]
