""" Functional TestCase Setup """
import datetime
from json import dumps, loads

import whatup_api.models as m
import whatup_api.tests.fixtures as fixtures
from whatup_api.tests import BaseApiTestCase


class FunctionalTestCase(BaseApiTestCase):

    post_headers = [('Content-Type', 'application/json')]

    # Set these in subclass
    expected_status = 404
    endpoint = '/api'

    @classmethod
    def setUpClass(cls):
        cls.client = cls.app.test_client()
        m.create_tables(cls.app)
        cls.fixture_data = fixtures.install(cls.app, *fixtures.all_data)

        cls.get_response()

    @classmethod
    def tearDownClass(cls):
        cls.db.session.remove()
        cls.db.drop_all()

    @classmethod
    def get_response(cls):
        if hasattr(cls, 'post_data'):
            cls.response = cls.client.post(
                cls.endpoint, data=dumps(cls.post_data),
                headers=cls.post_headers)

        elif hasattr(cls, 'put_data'):
            cls.response = cls.client.put(
                cls.endpoint, data=dumps(cls.put_data),
                headers=cls.post_headers)

        else:
            cls.response = cls.client.get(cls.endpoint)

        try:
            cls.json = loads(cls.response.data)
        except ValueError:
            cls.json = None

    @classmethod
    def compare_time(cls, value):
        expected = datetime.datetime.now()
        return abs(value - expected) < datetime.timedelta(minutes=1)

    def should_have_status(self, status=None):
        self.assertEqual(self.response.status_code, self.expected_status)
