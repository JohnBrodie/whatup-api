import datetime
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.orm.properties import RelationshipProperty

from whatup_api.tests import BaseApiTestCase
import whatup_api.models as m
import whatup_api.tests.fixtures as fixtures


class ModelTestCase(BaseApiTestCase):

    model = None
    columns = None
    relations = None

    @classmethod
    def setUpClass(cls):
        m.create_tables(cls.app)
        cls.data = fixtures.install(cls.app, *fixtures.all_data)
        cls.tag_data = cls.data.TagData
        cls.user_data = cls.data.UserData
        cls.post_data = cls.data.PostData
        cls.subscription_data = cls.data.SubscriptionData

        cls.model = getattr(m, cls.model_name)
        cls.columns, cls.relations = cls.get_columns_and_relations()

        for key, value in cls.post_data:
            setattr(cls, key, cls.db.session.query(cls.model)
                    .filter_by(id=cls.post_data[key].id).one())

    @classmethod
    def tearDownClass(cls):
        cls.db.session.remove()
        cls.db.drop_all()

    @classmethod
    def compare_time(cls, value):
        expected = datetime.datetime.now()
        return abs(value - expected) < datetime.timedelta(minutes=1)

    @classmethod
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

    def has_secondary(self, relation_name):
        return self.relations[relation_name].secondary.name

    #  Note: target is the target model's table name
    def has_target(self, relation_name):
        return self.relations[relation_name].target.name
