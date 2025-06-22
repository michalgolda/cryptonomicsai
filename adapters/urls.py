import os
import requests
from typing import override, Optional
from ports.urls import UrlsPort, UrlsData
from constants.asset import Asset


class CoinDeskUrlsAdapter(UrlsPort):
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.__api_key = api_key or os.environ.get("COINDESK_API_KEY")
        if self.__api_key is None:
            raise ValueError("The coindesk api key is required.")

    @override
    def get(self, asset: Asset) -> UrlsData:
        res = requests.get(
            f"https://data-api.coindesk.com/asset/v2/metadata?assets={asset.value}&asset_lookup_priority=SYMBOL&quote_asset=USD&asset_language=en-US&groups=RESOURCE_LINKS&api_key={self.__api_key}",
        )
        res = res.json()

        return UrlsData(
            website_url=res["Data"][asset.value]["WEBSITE_URL"],
            white_paper_url=res["Data"][asset.value]["WHITE_PAPER_URL"],
        )
