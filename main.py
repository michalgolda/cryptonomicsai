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
from indicators.dilution_risk import dilution_risk_indicator
from indicators.market_cap import market_cap_indicator
from indicators.unit_price import unit_price_indicator
from ports.community_sentiment import CommunitySentimentData


openai_client = openai.OpenAI()
firecrawl = FirecrawlApp()


def generate_summary(data: dict) -> str:
    chat_completions = openai_client.chat.completions.create(
        top_p=1,
        temperature=0.3,
        frequency_penalty=0.3,
        presence_penalty=0.1,
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a world-class crypto expert specialising in writing report based on provided data by user. You should only write based on data provided by user, don't use any other data. Don't limit words, if you need to write a little more text, do it. Use simple language, the final user is a average human. If you are not confident, don't use information or claim. Based on historical data, the most appropriate moment for enter the crypto market is when fear and greed index indicate fear on market. Your answer should contain only conclusion based on all provided data.",
            },
            {"role": "user", "content": json.dumps(data)},
        ],
    )
    summary = chat_completions.choices[0].message.content
    return summary


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

    general_asset_metadata = market_data_adapter.get_asset_metadata(Asset.SUI)
    fng_data = fng_source_adapter.get_fng()
    community_sentiment_data = failover_community_sentiment_adapter.get(Asset.SUI)

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
        },
        "general": {"fear_and_greed": fng_data.value_classification},
    }
    summary = generate_summary(data)
    print(summary)


if __name__ == "__main__":
    main()
