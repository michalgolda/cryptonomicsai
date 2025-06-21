from typing_extensions import override
from constants.asset import Asset
from ports.markets import MarketsPort, Market
from typing import List


class CoinLoreMarketsAdapter(MarketsPort):
    @override
    def get(self, asset: Asset) -> List[Market]:
        raise NotImplementedError
