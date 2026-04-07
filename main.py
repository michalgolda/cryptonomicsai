from firecrawl import FirecrawlApp

from adapters.cbbi import ColinTalksCryptoCBBIAdapter
from adapters.community_sentiment import (
    CoinGeckoCommunitySentimentAdapter,
    CoinMarketCapCommunitySentimentAdapter,
    FailoverCommunitySentimentAdapter,
)
from adapters.fng import AlternativeMeFNGSourceAdapter
from adapters.market_data import CoinLoreMarketDataAdapter
from adapters.security_metrics import CoindeskSecurityMetricAdapter
from adapters.top_markets import DropsTabTopMarketsAdapter
from ai import generate_summary
from constants.asset import Asset
from indicators.cbbi import cbbi_indicator
from indicators.dilution_risk import dilution_risk_indicator
from indicators.fng import fng_indicator
from indicators.market_cap import market_cap_indicator
from indicators.unit_price import unit_price_indicator

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
    cbbi_adapter = ColinTalksCryptoCBBIAdapter()

    general_asset_metadata = market_data_adapter.get_asset_metadata(Asset.BTC)
    fng_data = fng_source_adapter.get_fng()
    community_sentiment_data = failover_community_sentiment_adapter.get(Asset.BTC)
    security_metrics = coindesk_security_metric_adapter.get(Asset.BTC)
    top_markets = drops_tab_top_markets_adapter.get(Asset.BTC)
    cbbi_data = cbbi_adapter.get_cbbi()

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
        "general": {
            "fear_and_greed": fng_indicator(fng_data.value).value,
            "cbbi": cbbi_indicator(cbbi_data.value).value,
        },
    }
    result = generate_summary(data)
    print(f"Signal: {result['signal']}\nSummary: {result['summary']}")


if __name__ == "__main__":
    main()
