import requests
from typing import override
from ports.fng import FNGSourcePort, FNGData
from logger import get_logger

logger = get_logger(__name__)


class AlternativeMeFNGSourceAdapter(FNGSourcePort):
    @override
    def get_fng(self) -> FNGData:
        logger.info("Fetching Fear & Greed index from Alternative.me")
        res = requests.get("https://api.alternative.me/fng/")
        res = res.json()
        data = res.get("data")[0]
        fng = FNGData(value=float(data.get("value")))
        logger.info("Fear & Greed index: %.0f", fng.value)
        return fng
