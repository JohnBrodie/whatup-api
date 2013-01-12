import datetime
from unittest2 import TestCase

import whatup_api.models as m
from . import fixtures
from whatup_api.app import app, db


class _BaseApiTestCase(TestCase):
    """Create an instance of our app for all tests to use"""
    db = db
    app = app

    @classmethod
    def setUpClass(cls):
        cls.db.drop_all()
        cls.client = cls.app.test_client()
        m.create_tables(cls.app)
        cls.fixture_data = fixtures.install(cls.app, *fixtures.all_data)

    @classmethod
    def tearDownClass(cls):
        cls.db.session.remove()

    @classmethod
    def compare_time(cls, value):
        expected = datetime.datetime.now()
        return abs(value - expected) < datetime.timedelta(minutes=1)
