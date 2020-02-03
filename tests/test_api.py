from datetime import datetime
from http import HTTPStatus

import pytest

from fixerapp.models.currency_information import CurrencyInformation

@pytest.mark.usefixtures('testapp', 'database')
class TestApi:
    def test_rate_with_invalid_base(self, testapp, database):
        client = testapp.test_client()
        response = client.get('/rates/GBP')

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.text == 'Currency rate not supported'

    def test_rate_with_valid_base_and_no_date_filter(self, testapp, database):
        client = testapp.test_client()
        date = datetime.now().date()
        base = 'EUR'

        currency_information = CurrencyInformation(
            base_currency = base,
            changes = { 'GBP': 0.81 },
            change_date = date,
            retrieved_at = datetime.now()
        )

        database.session.add(currency_information)
        database.session.commit()

        response = client.get(f'/rates/{base}')

        assert response.status_code == HTTPStatus.OK
        assert response.json == { 'GBP': 0.81 }

    def test_rate_with_valid_base_and_a_date_filter(self, testapp, database):
        client = testapp.test_client()
        another_date = '2020-02-02'
        date = '2020-02-01'
        base = 'EUR'

        currency_information_prev = CurrencyInformation(
            base_currency = base,
            changes = { 'GBP': 0.81 },
            change_date = date,
            retrieved_at = datetime.now()
        )

        currency_information = CurrencyInformation(
            base_currency = base,
            changes = { 'GBP': 0.71 },
            change_date = another_date,
            retrieved_at = datetime.now()
        )

        database.session.add_all([currency_information_prev, currency_information])
        database.session.commit()

        response = client.get(f'/rates/{base}?date={date}')

        assert response.status_code == HTTPStatus.OK
        assert response.json == { 'GBP': 0.81 }

        response = client.get(f'/rates/{base}?date={another_date}')

        assert response.status_code == HTTPStatus.OK
        assert response.json == { 'GBP': 0.71 }
