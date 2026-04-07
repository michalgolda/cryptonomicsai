from curl_cffi import requests
from typing import override
from ports.cbbi import CBBISourcePort, CBBIData


class ColinTalksCryptoCBBIAdapter(CBBISourcePort):
    INDICATORS = ["PiCycle", "RUPL", "RHODL", "Puell", "2YMA", "Trolololo", "MVRV", "ReserveRisk", "Woobull"]

    @override
    def get_cbbi(self) -> CBBIData:
        data = requests.get("https://colintalkscrypto.com/cbbi/data/latest.json", impersonate="chrome").json()
        values = [next(reversed(indicator.values())) for key, indicator in data.items() if key in self.INDICATORS]
        cbbi = sum(values) / len(values) * 100

        return CBBIData(value=round(cbbi))
