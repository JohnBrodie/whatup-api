"""Test case for Tag model"""
from whatup_api.exceptions import APIError
import whatup_api.models as m

from whatup_api.tests.unit.models import ModelTestCase


class TagModelTestCase(ModelTestCase):
    """Tests for Tag model"""

    model_name = 'Tag'


class DescribePostModel(TagModelTestCase):
    def should_have_table_name(self):
        self.assertEquals(m.Post.__tablename__, 'posts')

    def should_have_id_as_pkey(self):
        self.assertTrue(self.is_primary_key('id'))


class DescribeIdColumn(TagModelTestCase):
    def should_have_id(self):
        self.assertEquals(self.Default.id, self.tag_data.Default.id)

    def should_have_id_as_integer(self):
        self.assertTrue(self.is_type('id', self.db.Integer))


class DescribeCreatedAtColumn(TagModelTestCase):
    def should_have_default_created_at(self):
        self.assertTrue(self.compare_time(self.SpecifiesNone.created_at))

    def should_have_created_at_as_datetime(self):
        self.assertTrue(self.is_type('created_at', self.db.DateTime))

    def should_have_non_nullable_created_at(self):
        self.assertFalse(self.is_nullable('created_at'))


class DescribeModifiedAtColumn(TagModelTestCase):
    def should_have_modified_at(self):
        self.assertEquals(self.Default.modified_at,
                          self.tag_data.Default.modified_at)

    def should_have_modified_at_as_datetime(self):
        self.assertTrue(self.is_type('modified_at', self.db.DateTime))

    def should_have_non_nullable_modified_at(self):
        self.assertFalse(self.is_nullable('modified_at'))

    def should_have_default_modified_at(self):
        self.assertTrue(self.compare_time(self.SpecifiesNone.modified_at))


class DescribeNameColumn(TagModelTestCase):
    def should_have_name(self):
        self.assertEquals(self.Default.name, self.tag_data.Default.name)

    def should_have_name_as_string(self):
        self.assertTrue(self.is_type('name', self.db.String))

    def should_have_name_with_length(self):
        self.assertEquals(self.get_length('name'), 100)

    def should_have_non_nullable_name(self):
        self.assertFalse(self.is_nullable('name'))


class DescribeSummaryColumn(TagModelTestCase):
    def should_have_summary(self):
        self.assertEquals(self.Default.summary, self.tag_data.Default.summary)

    def should_have_summary_as_string(self):
        self.assertTrue(self.is_type('summary', self.db.String))

    def should_have_summary_with_length(self):
        self.assertEquals(self.get_length('summary'), 100)


class DescribeAuthorRelationship(TagModelTestCase):
    def should_have_author(self):
        author = self.Default.author
        self.assertEqual(author.id, self.user_data.Default.id)


class DescribeValidators(TagModelTestCase):
    def should_have_name_validation_return_name(self):
        name = 'name here'
        returned_name = m.Tag.validate_name(
            m.Tag(), 'name', name)
        self.assertEqual(returned_name, name)

    def should_raise_error_on_null_name(self):
        with self.assertRaises(APIError) as cm:
            m.Tag.validate_name(
                m.Tag(), 'name', None)

        error = cm.exception.errors
        self.assertEqual(error['name'], 'Must specify name')
