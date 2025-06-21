import requests
from constants.asset import Asset, AssetName
from ports.top_markets import TopMarketsPort, Market
from typing import List, override


class DropsTabTopMarketsAdapter(TopMarketsPort):
    def __get_asset_name(self, asset: Asset) -> str:
        return AssetName[asset.value].value

    @override
    def get(self, asset: Asset) -> List[Market]:
        asset_name = self.__get_asset_name(asset)
        res = requests.get(
            f"https://api2.icodrops.com/portfolio/api/exchange/{asset_name}/topMarkets"
        )
        res = res.json()

        return [
            Market(exchange_name=m.get("exchangeName"), volume24h=m.get("volume24h"))
            for m in res
        ]
