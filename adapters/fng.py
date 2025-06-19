import requests
from typing import override
from ports.fng import FNGSourcePort, FNGData


class AlternativeMeFNGSourceAdapter(FNGSourcePort):
    @override
    def get_fng(self) -> FNGData:
        res = requests.get("https://api.alternative.me/fng/")
        res = res.json()
        data = res.get("data")[0]

        return FNGData(
            value=float(data.get("value")),
            value_classification=data.get("value_classification"),
        )
