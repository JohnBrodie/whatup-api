import datetime
from unittest2 import TestCase

import whatup_api.models as m
from . import fixtures
from whatup_api.hello import app


class _BaseApiTestCase(TestCase):
    """Create an instance of our app for all tests to use"""
    db_uri = 'mysql://root:whatup@localhost/tests'
    db = m.init_app(app)
    app = app

    @classmethod
    def setUpClass(cls):
        cls.client = cls.app.test_client()
        m.create_tables(cls.app)
        cls.fixture_data = fixtures.install(cls.app, *fixtures.all_data)

    @classmethod
    def tearDownClass(cls):
        cls.db.session.remove()
        cls.db.drop_all()

    @classmethod
    def compare_time(cls, value):
        expected = datetime.datetime.now()
        return abs(value - expected) < datetime.timedelta(minutes=1)
