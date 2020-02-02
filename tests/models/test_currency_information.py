import pytest

from datetime import datetime
from dateutil import parser

from fixerapp import db
from fixerapp.models.currency_information import CurrencyInformation

@pytest.mark.usefixtures('database')
class TestCurrencyInformation:

    def test_latest_rates_when_no_date_provided_and_only_one_available(self, database):
        base = 'EUR'
        currency_information = CurrencyInformation(
            base_currency = base,
            changes = { 'GBP': 0.81 },
            change_date = '2020-02-02',
            retrieved_at = datetime.now()
        )

        db.session.add(currency_information)
        db.session.commit()

        latest_rate = CurrencyInformation.latest_rates(base)

        assert  latest_rate.base_currency == currency_information.base_currency
        assert  latest_rate.changes == currency_information.changes
        assert  latest_rate.change_date == currency_information.change_date
        assert  latest_rate.retrieved_at == currency_information.retrieved_at

    def test_latest_rates_when_no_date_provided_and_multiple_available(self, database):
        base = 'EUR'
        currency_information_prev = CurrencyInformation(
            base_currency = base,
            changes = { 'GBP': 0.81 },
            change_date = '2020-02-02',
            retrieved_at = datetime.now()
        )

        db.session.add(currency_information_prev)
        db.session.commit()

        currency_information = CurrencyInformation(
            base_currency = base,
            changes = { 'GBP': 0.84, 'CAD': 1.45 },
            change_date = '2020-02-02',
            retrieved_at = datetime.now()
        )

        db.session.add(currency_information)
        db.session.commit()

        latest_rate = CurrencyInformation.latest_rates(base)

        assert  latest_rate.base_currency == currency_information.base_currency
        assert  latest_rate.changes == currency_information.changes
        assert  latest_rate.change_date == currency_information.change_date
        assert  latest_rate.retrieved_at == currency_information.retrieved_at

    def test_latest_rates_when_date_provided_and_multiple_available(self, database):
        base = 'EUR'
        date = '2020-02-01'

        currency_information_prev = CurrencyInformation(
            base_currency = base,
            changes = { 'GBP': 0.81 },
            change_date = date,
            retrieved_at = datetime.now()
        )

        db.session.add(currency_information_prev)
        db.session.commit()

        currency_information = CurrencyInformation(
            base_currency = base,
            changes = { 'GBP': 0.84, 'CAD': 1.45 },
            change_date = '2020-02-02',
            retrieved_at = datetime.now()
        )

        db.session.add(currency_information)
        db.session.commit()

        latest_rate = CurrencyInformation.latest_rates(base, date=parser.parse(date).date())

        assert  latest_rate.base_currency == currency_information_prev.base_currency
        assert  latest_rate.changes == currency_information_prev.changes
        assert  latest_rate.change_date == currency_information_prev.change_date
        assert  latest_rate.retrieved_at == currency_information_prev.retrieved_at
