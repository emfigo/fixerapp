import os
import requests

class FixerClient:
    MAYOR_CURRENCIES = [
        'USD',
        'AUD',
        'CAD',
        'PLN',
        'MXN',
        'GBP'
    ]

    @classmethod
    def latest_rates(cls):
        payload = {
            'access_key': os.environ.get('FIXER_API_KEY'),
            'symbols': ','.join(cls.MAYOR_CURRENCIES),
            'format': 1
        }

        return requests.get(f'{cls.url()}/latest', params=payload).json()

    @staticmethod
    def url():
        return os.environ.get('FIXER_URL')
