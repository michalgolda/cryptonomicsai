from typing import override

import requests
from ports.market_data import MarketDataPort, Asset, GeneralAssetMetadata


class CoinLoreMarketDataAdapter(MarketDataPort):
    def __get_asset_id(self, asset: Asset) -> str:
        assets = {Asset.BTC: "90", Asset.ETH: "80"}
        if asset not in assets:
            raise ValueError(f"{asset.value} is not supported by CoinLore")

        return assets[asset]

    @override
    def get_asset_metadata(self, asset: Asset) -> GeneralAssetMetadata:
        asset_id = self.__get_asset_id(asset)

        res = requests.get(f"https://api.coinlore.net/api/ticker/?id={asset_id}")
        res = res.json()[0]

        return GeneralAssetMetadata(
            name=res.get("name"),
            total_supply=round(float(res.get("tsupply")), 2),
            circulating_supply=round(float(res.get("csupply")), 2),
        )
