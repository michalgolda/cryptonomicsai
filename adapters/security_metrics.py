import os
from typing import List, override, Optional
import requests
from ports.security_metrics import SecurityMetricPort, SecurityMetricData
from constants.asset import Asset


class CoindeskSecurityMetricAdapter(SecurityMetricPort):
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.__api_key = api_key or os.environ.get("COINDESK_API_KEY")
        if self.__api_key is None:
            raise ValueError("The coindesk api key is required.")

    @override
    def get(self, asset: Asset) -> List[SecurityMetricData]:
        res = requests.get(
            f"https://data-api.coindesk.com/asset/v2/metadata?assets={asset.value}&asset_lookup_priority=SYMBOL&quote_asset=USD&asset_language=en-US&groups=SECURITY_METRICS&api_key={self.__api_key}",
        )
        res = res.json()

        return [
            SecurityMetricData(name=m.get("NAME"), score=m.get("OVERALL_SCORE"))
            for m in res["Data"][asset.value]["ASSET_SECURITY_METRICS"]
        ]
