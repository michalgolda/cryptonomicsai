import json
import openai
from firecrawl import FirecrawlApp
from adapters.market_data import CoinLoreMarketDataAdapter
from constants.asset import Asset
from adapters.fng import AlternativeMeFNGSourceAdapter
from adapters.community_sentiment import (
    CoinGeckoCommunitySentimentAdapter,
    CoinMarketCapCommunitySentimentAdapter,
    FailoverCommunitySentimentAdapter,
)
from ai import generate_summary
from indicators.dilution_risk import dilution_risk_indicator
from indicators.market_cap import market_cap_indicator
from indicators.unit_price import unit_price_indicator
from adapters.security_metrics import CoindeskSecurityMetricAdapter


firecrawl = FirecrawlApp()


def main():
    fng_source_adapter = AlternativeMeFNGSourceAdapter()
    market_data_adapter = CoinLoreMarketDataAdapter()
    coinmarketcap_community_sentiment_adapter = CoinMarketCapCommunitySentimentAdapter(
        firecrawl
    )
    coingecko_community_sentiment_adapter = CoinGeckoCommunitySentimentAdapter()
    failover_community_sentiment_adapter = FailoverCommunitySentimentAdapter(
        [
            coingecko_community_sentiment_adapter,
            coinmarketcap_community_sentiment_adapter,
        ]
    )
    coindesk_security_metric_adapter = CoindeskSecurityMetricAdapter()

    general_asset_metadata = market_data_adapter.get_asset_metadata(Asset.TRX)
    fng_data = fng_source_adapter.get_fng()
    community_sentiment_data = failover_community_sentiment_adapter.get(Asset.TRX)
    security_metrics = coindesk_security_metric_adapter.get(Asset.TRX)

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
        },
        "general": {"fear_and_greed": fng_data.value_classification},
    }
    summary = generate_summary(data)
    print(summary)


if __name__ == "__main__":
    main()
