import json
from flask import Response
from flask.testing import FlaskClient
import pytest

from sqlalchemy.orm import Session
from fixerapp import app, db
from fixerapp.api import rates


@pytest.fixture(scope='session')
def database(request):
    db.create_all()

    yield db

    @request.addfinalizer
    def drop_database():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='session')
def testapp():
    app.config['TESTING'] = True
    app.response_class = MyResponse
    app.test_client_class = FlaskClient

    app.register_blueprint(rates)
    return app

class MyResponse(Response):
    """Implements custom deserialisation method for response objects"""

    @property
    def text(self):
        return self.get_data(as_text=True)

    @property
    def json(self):
        return json.loads(self.text)

