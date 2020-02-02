from datetime import datetime
from unittest.mock import MagicMock
import pytest

from fixerapp.models.currency_information import CurrencyInformation
from fixerapp.rate_ingestor import RateIngestor


from tests.helpers import PrintCapture


@pytest.mark.usefixtures('database')
class TestRateIngestor:
    def test_process_with_correct_values(self, database):
        latest_rate = {
            'base': 'EUR',
            'rates': { 'GBP': 1.41 },
            'date': '2015-02-02',
            'timestamp': int(datetime.now().timestamp())
        }
        client = MagicMock()
        client.latest_rates = MagicMock(return_value=latest_rate)

        RateIngestor.process(client=client)

        assert CurrencyInformation.query.filter_by(change_date='2015-02-02').count() == 1

        rate = CurrencyInformation.query.filter_by(change_date='2015-02-02').first()

        assert  rate.base_currency == latest_rate['base']
        assert  rate.changes == latest_rate['rates']
        assert  rate.change_date.strftime("%Y-%m-%d") == latest_rate['date']
        assert  int(rate.retrieved_at.timestamp()) == latest_rate['timestamp']

    def test_process_with_duplicated_values(self, database):
        latest_rate = {
            'base': 'EUR',
            'rates': { 'GBP': 0.81 },
            'date': '2020-02-02',
            'timestamp': 1580656619
        }
        client = MagicMock()
        client.latest_rates = MagicMock(return_value=latest_rate)

        RateIngestor.process(client=client)

        with PrintCapture(line_filter='Error ingesting rate') as out:
            RateIngestor.process(client=client)
            assert len(out.lines) == 1
