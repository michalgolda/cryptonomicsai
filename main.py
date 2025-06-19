import os
import json
import openai
from adapters.market_data import CoinLoreMarketDataAdapter
from indicators.dilution_risk import dilution_risk_indicator
from indicators.market_cap import market_cap_indicator
from indicators.unit_price import unit_price_indicator
from constants.asset import Asset


openai_client = openai.OpenAI()


def generate_summary(data: dict) -> str:
    chat_completions = openai_client.chat.completions.create(
        top_p=1,
        temperature=0.5,
        frequency_penalty=0.3,
        presence_penalty=0.1,
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a world-class crypto expert specialising in writing report based on provided data by user. You should only write based on data provided by user, don't use any other data. Don't limit words, if you need to write a little more text, do it. Use simple language, the final user is a average human. If you are not confident, don't use information or claim.",
            },
            {"role": "user", "content": json.dumps(data)},
        ],
    )
    summary = chat_completions.choices[0].message.content
    return summary


def main():
    market_data_adapter = CoinLoreMarketDataAdapter()
    general_asset_metadata = market_data_adapter.get_asset_metadata(Asset.SUI)

    data = {
        "asset_name": general_asset_metadata.name,
        "unit_price_category": unit_price_indicator(general_asset_metadata.price),
        "market_cap_category": market_cap_indicator(general_asset_metadata.market_cap),
        "dilution_risk": dilution_risk_indicator(
            general_asset_metadata.total_supply,
            general_asset_metadata.circulating_supply,
        ),
    }
    summary = generate_summary(data)
    print(summary)


if __name__ == "__main__":
    main()
