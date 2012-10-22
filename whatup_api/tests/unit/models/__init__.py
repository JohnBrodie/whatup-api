import os

from flask import Flask
from flask.ext.testing import TestCase

import whatup_api.models as m
import whatup_api.tests.fixtures as fixtures


class ModelTestCase(TestCase):

    db_uri = 'sqlite:///' + os.path.abspath('../../tests.db')

    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        return app

    def setUp(self):
        m.create_tables(self.app)
        fixtures.install(self.app, *fixtures.all_data)
        self.db = m.init_app(self.app)

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

