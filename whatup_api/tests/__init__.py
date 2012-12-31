from unittest2 import TestCase

import whatup_api.models as m
from whatup_api.hello import app


class BaseApiTestCase(TestCase):
    """Create an instance of our app for all tests to use"""
    db_uri = 'mysql://root:whatup@localhost/tests'
    db = m.init_app(app)
    app = app
