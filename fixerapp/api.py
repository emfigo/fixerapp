from datetime import datetime
from dateutil import parser
from flask import Blueprint, request, jsonify
from http import HTTPStatus

from fixerapp import app
from fixerapp.models.currency_information import CurrencyInformation

rates = Blueprint('rates', __name__)

@rates.route('/rates/<base>')
def rate(base):
    if base != 'EUR':
        return 'Currency rate not supported', HTTPStatus.NOT_FOUND

    if request.args.get('date'):
        filter_date = parser.parse(request.args.get('date')).date()
    else:
        filter_date = datetime.now().date()

    rates = CurrencyInformation.latest_rates(base, date=filter_date)
    if rates:
        rates = rates.changes
    else:
        rates = {}

    return jsonify(rates), HTTPStatus.OK

