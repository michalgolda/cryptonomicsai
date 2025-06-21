from typing import override

import requests
from constants.asset import Asset
from ports.market_data import MarketDataPort, GeneralAssetMetadata


class CoinLoreMarketDataAdapter(MarketDataPort):
    def __get_asset_id(self, asset: Asset) -> str:
        assets = {
            Asset.BTC: "90",
            Asset.ETH: "80",
            Asset.TRX: "2713",
            Asset.SUI: "93845",
            Asset.BEAM: "136107",
        }
        if asset not in assets:
            raise ValueError(f"Can not determine asset id of {asset.value}")

        return assets[asset]

    @override
    def get_asset_metadata(self, asset: Asset) -> GeneralAssetMetadata:
        asset_id = self.__get_asset_id(asset)

        res = requests.get(f"https://api.coinlore.net/api/ticker/?id={asset_id}")
        res = res.json()[0]

        return GeneralAssetMetadata(
            name=res.get("name"),
            price=round(float(res.get("price_usd")), 2),
            market_cap=round(float(res.get("market_cap_usd")), 2),
            total_supply=round(float(res.get("tsupply")), 2),
            circulating_supply=round(float(res.get("csupply")), 2),
        )
