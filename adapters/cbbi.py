from curl_cffi import requests
from typing import override
from ports.cbbi import CBBISourcePort, CBBIData
from logger import get_logger

logger = get_logger(__name__)


class ColinTalksCryptoCBBIAdapter(CBBISourcePort):
    INDICATORS = ["PiCycle", "RUPL", "RHODL", "Puell", "2YMA", "Trolololo", "MVRV", "ReserveRisk", "Woobull"]

    @override
    def get_cbbi(self) -> CBBIData:
        logger.info("Fetching CBBI data from ColintalksCrypto")
        data = requests.get("https://colintalkscrypto.com/cbbi/data/latest.json", impersonate="chrome").json()
        values = [next(reversed(indicator.values())) for key, indicator in data.items() if key in self.INDICATORS]
        cbbi = CBBIData(value=round(sum(values) / len(values) * 100))
        logger.info("CBBI value: %d", cbbi.value)
        return cbbi
