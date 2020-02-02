import re
import requests_mock

from fixerapp.fixer_client import FixerClient

class TestFixerClient:
    def test_latest_rates(self):
        response ={
            "success": True,
            "timestamp": 1580577185,
            "base": "EUR",
            "date": "2020-02-01",
            "rates": {
                "USD": 1.10943,
                "AUD": 1.65735,
                "CAD": 1.468314,
                "PLN": 4.296716,
                "MXN": 20.905659,
                "GBP": 0.840185
            }
        }

        matcher = re.compile(f'{FixerClient.url()}[?.]*')
        with requests_mock.mock() as m:
            m.get(matcher, json=response)
            assert response ==FixerClient.latest_rates()
