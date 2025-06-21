import requests
from typing import override
from pydantic import BaseModel
from firecrawl import FirecrawlApp, JsonConfig
from ports.community_sentiment import CommunitySentimentPort, CommunitySentimentData
from constants.asset import Asset, AssetName


class FirecrawlExtractionSchema(BaseModel):
    bullish: int
    bearish: int


class CoinMarketCapCommunitySentimentAdapter(CommunitySentimentPort):
    def __init__(self, firecrawl: FirecrawlApp) -> None:
        self.__firecrawl = firecrawl

    def get(self, asset: Asset) -> CommunitySentimentData:
        json_config = JsonConfig(schema=FirecrawlExtractionSchema)
        extraction_result = self.__firecrawl.scrape_url(
            url=f"https://coinmarketcap.com/currencies/{asset.value.lower()}/",
            formats=["json"],
            only_main_content=True,
            include_tags=[".ratio"],
            mobile=True,
            wait_for=2000,
            json_options=json_config,
        )
        return CommunitySentimentData(
            bullish=extraction_result.json.get("bullish"),
            bearish=extraction_result.json.get("bearish"),
        )


class CoinGeckoCommunitySentimentAdapter(CommunitySentimentPort):
    def __get_asset_name(self, asset: Asset) -> str:
        return AssetName[asset.value].value

    @override
    def get(self, asset: Asset) -> CommunitySentimentData:
        asset_name = self.__get_asset_name(asset)
        res = requests.get(
            f"https://www.coingecko.com/sentiment_votes/voted_coin_today?api_symbol={asset_name}"
        )
        res = res.json()

        return CommunitySentimentData(
            bullish=int(res.get("percentage").get("positive")),
            bearish=int(res.get("percentage").get("negative")),
        )


