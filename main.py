import json
import openai
from adapters.market_data import CoinLoreMarketDataAdapter
from indicators.dilution_risk import dilution_risk_indicator
from indicators.market_cap import market_cap_indicator
from indicators.unit_price import unit_price_indicator
from constants.asset import Asset
from adapters.fng import AlternativeMeFNGSourceAdapter


openai_client = openai.OpenAI()


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

    general_asset_metadata = market_data_adapter.get_asset_metadata(Asset.TRX)
    fng_data = fng_source_adapter.get_fng()

    data = {
        "asset_specific": {
            "asset_name": general_asset_metadata.name,
            "unit_price_category": unit_price_indicator(general_asset_metadata.price),
            "market_cap_category": market_cap_indicator(
                general_asset_metadata.market_cap
            ),
            "dilution_risk": dilution_risk_indicator(
                general_asset_metadata.total_supply,
                general_asset_metadata.circulating_supply,
            ),
        },
        "general": {"fear_and_greed": fng_data.value_classification},
    }
    summary = generate_summary(data)
    print(summary)


if __name__ == "__main__":
    main()
