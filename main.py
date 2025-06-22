from firecrawl import FirecrawlApp
from adapters.market_data import CoinLoreMarketDataAdapter
from adapters.urls import CoinDeskUrlsAdapter
from constants.asset import Asset
from adapters.fng import AlternativeMeFNGSourceAdapter
from adapters.community_sentiment import (
    CoinGeckoCommunitySentimentAdapter,
    CoinMarketCapCommunitySentimentAdapter,
    FailoverCommunitySentimentAdapter,
)
from adapters.urls import CoinDeskUrlsAdapter
from ai import generate_summary
from indicators.dilution_risk import dilution_risk_indicator
from indicators.market_cap import market_cap_indicator
from indicators.unit_price import unit_price_indicator
from adapters.security_metrics import CoindeskSecurityMetricAdapter
from adapters.top_markets import DropsTabTopMarketsAdapter


firecrawl = FirecrawlApp()


def main():
    fng_source_adapter = AlternativeMeFNGSourceAdapter()
    market_data_adapter = CoinLoreMarketDataAdapter()
    coinmarketcap_community_sentiment_adapter = CoinMarketCapCommunitySentimentAdapter(
        firecrawl
    )
    drops_tab_top_markets_adapter = DropsTabTopMarketsAdapter()
    coingecko_community_sentiment_adapter = CoinGeckoCommunitySentimentAdapter()
    failover_community_sentiment_adapter = FailoverCommunitySentimentAdapter(
        [
            coingecko_community_sentiment_adapter,
            coinmarketcap_community_sentiment_adapter,
        ]
    )
    coindesk_security_metric_adapter = CoindeskSecurityMetricAdapter()
    coindesk_urls_adapter = CoinDeskUrlsAdapter()

    general_asset_metadata = market_data_adapter.get_asset_metadata(Asset.ETH)
    fng_data = fng_source_adapter.get_fng()
    community_sentiment_data = failover_community_sentiment_adapter.get(Asset.ETH)
    security_metrics = coindesk_security_metric_adapter.get(Asset.ETH)
    top_markets = drops_tab_top_markets_adapter.get(Asset.ETH)
    urls = coindesk_urls_adapter.get(Asset.ETH)

    data = {
        "asset_specific": {
            "asset_name": general_asset_metadata.name,
            "unit_price_category": unit_price_indicator(
                general_asset_metadata.price
            ).value,
            "market_cap_category": market_cap_indicator(
                general_asset_metadata.market_cap
            ).value,
            "dilution_risk": dilution_risk_indicator(
                general_asset_metadata.total_supply,
                general_asset_metadata.circulating_supply,
            ).value,
            "community_sentiment": {
                "bearish": community_sentiment_data.bearish,
                "bullish": community_sentiment_data.bullish,
            },
            "security_metrics": [
                {"name": m.name, "score": m.score} for m in security_metrics
            ],
            "top_markets": [{"exchange_name": m.exchange_name} for m in top_markets],
        },
        "general": {"fear_and_greed": fng_data.value_classification},
    }
    summary = generate_summary(data)
    print(summary)


if __name__ == "__main__":
    main()
