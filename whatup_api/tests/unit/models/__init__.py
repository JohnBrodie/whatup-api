from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.orm.properties import RelationshipProperty

from whatup_api.tests import _BaseApiTestCase
import whatup_api.models as m


class _ModelTestCase(_BaseApiTestCase):

    model = None
    columns = None
    relations = None

    @classmethod
    def setUpClass(cls):
        super(_ModelTestCase, cls).setUpClass()
        cls.tag_data = cls.fixture_data.TagData
        cls.user_data = cls.fixture_data.UserData
        cls.post_data = cls.fixture_data.PostData
        cls.subscription_data = cls.fixture_data.SubscriptionData

        cls.model_data = cls.fixture_data[cls.model_name + 'Data']
        cls.model = getattr(m, cls.model_name)
        cls.columns, cls.relations = cls.get_columns_and_relations()

        for key, value in cls.model_data:
            setattr(cls, key, cls.db.session.query(cls.model)
                    .filter_by(id=cls.model_data[key].id).one())

    @classmethod
    def get_columns_and_relations(cls):
        fields = set(cls.model._sa_class_manager.values())
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

    # TODO move these tests somewhere and use multiple inheritence?
    def should_have_table_name(self):
        expected_table_name = '{0}s'.format(self.model_name.lower())
        self.assertEqual(self.model.__tablename__, expected_table_name)

    def should_have_id_as_pkey(self):
        self.assertTrue(self.is_primary_key('id'))

    def should_have_id(self):
        self.assertEquals(self.Default.id, self.model_data.Default.id)

    def should_have_id_as_integer(self):
        self.assertTrue(self.is_type('id', self.db.Integer))

    def should_have_default_created_at(self):
        self.assertTrue(self.compare_time(self.SpecifiesNone.created_at))

    def should_have_created_at_as_datetime(self):
        self.assertTrue(self.is_type('created_at', self.db.DateTime))

    def should_have_non_nullable_created_at(self):
        self.assertFalse(self.is_nullable('created_at'))

    def should_have_modified_at(self):
        self.assertEquals(self.Default.modified_at,
                          self.model_data.Default.modified_at)

    def should_have_modified_at_as_datetime(self):
        self.assertTrue(self.is_type('modified_at', self.db.DateTime))

    def should_have_non_nullable_modified_at(self):
        self.assertFalse(self.is_nullable('modified_at'))

    def should_have_default_modified_at(self):
        self.assertTrue(self.compare_time(self.SpecifiesNone.modified_at))

    def should_have_is_deleted(self):
        self.assertEqual(self.Default.is_deleted,
                         self.model_data.Default.is_deleted)

    def should_have_non_nullable_is_deleted(self):
        self.assertFalse(self.is_nullable('is_deleted'))

    def should_have_default_is_deleted(self):
        self.assertFalse(self.SpecifiesNone.is_deleted)

    def should_have_is_deleted_as_boolean(self):
        self.assertTrue(self.is_type('is_deleted', self.db.Boolean))

    # TODO move these to tests/helpers
    @classmethod
    def is_primary_key(cls, column_name):
        return cls.columns[column_name].primary_key

    @classmethod
    def is_nullable(cls, column_name):
        return cls.columns[column_name].nullable

    @classmethod
    def is_type(cls, column_name, type_):
        return isinstance(cls.columns[column_name].type, type_)

    @classmethod
    def get_length(cls, column_name):
        return cls.columns[column_name].type.length

    @classmethod
    def is_lazy(cls, relation_name):
        return cls.relations[relation_name].lazy

    @classmethod
    def has_backref(cls, relation_name):
        return cls.relations[relation_name].backref

    @classmethod
    def has_secondary(cls, relation_name):
        return cls.relations[relation_name].secondary.name

    #  Note: target is the target model's table name
    @classmethod
    def has_target(cls, relation_name):
        return cls.relations[relation_name].target.name
