"""Test case for Tag model"""
import whatup_api.models as m

from whatup_api.tests.unit.models import ModelTestCase


class TagModelTestCase(ModelTestCase):
    """Tests for Tag model"""

    def setUp(self):
        super(TagModelTestCase, self).setUp()
        self.model = m.Tag
        self.columns, self.relations = self.get_columns_and_relations()

        self.tag = self.db.session.query(m.Tag) \
            .filter_by(id=self.tag_data.Default.id).one()
        self.specifies_none = self.db.session.query(m.Post) \
            .filter_by(id=self.tag_data.SpecifiesNone.id).one()

    def tearDown(self):
        super(TagModelTestCase, self).tearDown()

class DescribePostModel(TagModelTestCase):
    def should_have_table_name(self):
        self.assertEquals(m.Post.__tablename__, 'posts')

    def should_have_id_as_pkey(self):
        self.assertTrue(self.is_primary_key('id'))

class DescribeIdColumn(TagModelTestCase):
    def should_have_id(self):
        self.assertEquals(self.tag.id, self.tag_data.Default.id)

    def should_have_id_as_integer(self):
        self.assertTrue(self.is_type('id', self.db.Integer))

class DescribeCreatedAtColumn(TagModelTestCase):
    def should_have_default_created_at(self):
        self.assertTrue(self.compare_time(self.specifies_none.created_at))

    def should_have_created_at_as_datetime(self):
        self.assertTrue(self.is_type('created_at', self.db.DateTime))

    def should_have_non_nullable_created_at(self):
        self.assertFalse(self.is_nullable('created_at'))

class DescribeModifiedAtColumn(TagModelTestCase):
    def should_have_modified_at(self):
        self.assertEquals(self.tag.modified_at,
                          self.tag_data.Default.modified_at)

    def should_have_modified_at_as_datetime(self):
        self.assertTrue(self.is_type('modified_at', self.db.DateTime))

    def should_have_non_nullable_modified_at(self):
        self.assertFalse(self.is_nullable('modified_at'))

    def should_have_default_modified_at(self):
        self.assertTrue(self.compare_time(self.specifies_none.modified_at))

class DescribeNameColumn(TagModelTestCase):
    def should_have_name(self):
        self.assertEquals(self.tag.name, self.tag_data.Default.name)

    def should_have_name_as_string(self):
        self.assertTrue(self.is_type('name', self.db.String))

    def should_have_name_with_length(self):
        self.assertEquals(self.get_length('name'), 100)

    def should_have_non_nullable_name(self):
        self.assertFalse(self.is_nullable('name'))

class DescribeSummaryColumn(TagModelTestCase):
    def should_have_summary(self):
        self.assertEquals(self.tag.summary, self.tag_data.Default.summary)

    def should_have_summary_as_string(self):
        self.assertTrue(self.is_type('summary', self.db.String))

    def should_have_summary_with_length(self):
        self.assertEquals(self.get_length('summary'), 100)

class DescribeAuthorRelationship(TagModelTestCase):
    def should_have_author(self):
        author = self.tag.author
        self.assertEqual(author.id, self.user_data.Default.id)
