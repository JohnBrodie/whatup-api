from flask import Flask
from flask.ext.testing import TestCase

import whatup_api.models as m
import whatup_api.tests.fixtures as fixtures


class ModelTestCase(TestCase):

    db_uri = 'mysql://root:whatup@localhost/tests'

    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        return app

    def setUp(self):
        m.create_tables(self.app)
        self.data = fixtures.install(self.app, *fixtures.all_data)
        self.db = m.init_app(self.app)
        self.tag_data = self.data.TagData
        self.user_data = self.data.UserData
        self.post_data = self.data.PostData
        self.subscription_data = self.data.SubscriptionData

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
