import datetime
from flask import Flask
from flask.ext.testing import TestCase
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.orm.properties import RelationshipProperty

import whatup_api.models as m
import whatup_api.tests.fixtures as fixtures


class ModelTestCase(TestCase):

    db_uri = 'mysql://root:whatup@localhost/tests'
    model = None
    columns = None
    relations = None

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

    def compare_time(self, value):
        expected = datetime.datetime.now()
        return abs(value - expected) < datetime.timedelta(minutes=1)

    def get_columns_and_relations(self):
        fields = set(self.model._sa_class_manager.values())
        columns = {}
        relations = {}
        for field in fields:
            prop = field.property
            if isinstance(prop, ColumnProperty):
                column = prop.columns[0]
                columns[column.name] = column
            elif isinstance(prop, RelationshipProperty):
                relation = prop
                relations[relation.key] = relation
        return (columns, relations)

    def is_primary_key(self, column_name):
        return self.columns[column_name].primary_key

    def is_nullable(self, column_name):
        return self.columns[column_name].nullable

    def is_type(self, column_name, type_):
        return isinstance(self.columns[column_name].type, type_)

    def get_length(self, column_name):
        return self.columns[column_name].type.length

    def is_lazy(self, relation_name):
        return self.relations[relation_name].lazy

    def has_backref(self, relation_name):
        return self.relations[relation_name].backref

    #  Note: target is the target model's table name
    def has_target(self, relation_name):
        return self.relations[relation_name].target.name
