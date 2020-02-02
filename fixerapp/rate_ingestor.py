from fixerapp import db
from fixerapp.fixer_client import FixerClient
from fixerapp.models.currency_information import CurrencyInformation

from datetime import datetime
from sqlalchemy.exc import IntegrityError

class RateIngestor:
    @staticmethod
    def process(client = FixerClient):
        rates = client.latest_rates()

        currency_information = CurrencyInformation(
            base_currency = rates['base'],
            changes = rates['rates'],
            change_date = rates['date'],
            retrieved_at = datetime.fromtimestamp(rates['timestamp'])
        )

        try:
            db.session.add(currency_information)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            print(f'Error ingesting rate:\n {e}')
