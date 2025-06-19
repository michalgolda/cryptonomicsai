from adapters.market_data import CoinLoreMarketDataAdapter
from indicators.dilution_risk import dilution_risk_indicator
from ports.market_data import Asset


def main():
    market_data_adapter = CoinLoreMarketDataAdapter()
    general_asset_metadata = market_data_adapter.get_asset_metadata(Asset.ETH)
    print(
        "Dilution Risk: ",
        dilution_risk_indicator(
            total_supply=general_asset_metadata.total_supply,
            circulating_supply=general_asset_metadata.circulating_supply,
        ),
    )


if __name__ == "__main__":
    main()
