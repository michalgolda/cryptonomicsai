from adapters.market_data import CoinLoreMarketDataAdapter
from indicators.dilution_risk import dilution_risk_indicator
from indicators.market_cap import market_cap_indicator
from indicators.unit_price import unit_price_indicator
from constants.asset import Asset


def main():
    market_data_adapter = CoinLoreMarketDataAdapter()
    general_asset_metadata = market_data_adapter.get_asset_metadata(Asset.SUI)
    print("Asset name: ", general_asset_metadata.name)
    print("Unit price category: ", unit_price_indicator(general_asset_metadata.price))
    print(
        "Market Cap Category: ", market_cap_indicator(general_asset_metadata.market_cap)
    )
    print(
        "Dilution Risk: ",
        dilution_risk_indicator(
            total_supply=general_asset_metadata.total_supply,
            circulating_supply=general_asset_metadata.circulating_supply,
        ),
    )


if __name__ == "__main__":
    main()
