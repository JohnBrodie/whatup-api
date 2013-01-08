"""Test case for Tag model"""
from whatup_api.exceptions import APIError
import whatup_api.models as m

from whatup_api.tests.unit.models import _ModelTestCase


class TagModelTestCase(_ModelTestCase):
    """Tests for Tag model"""

    model_name = 'Tag'


class DescribePostModel(TagModelTestCase):

    def should_have_name(self):
        self.assertEquals(self.Default.name, self.tag_data.Default.name)

    def should_have_name_as_string(self):
        self.assertTrue(self.is_type('name', self.db.String))

    def should_have_name_with_length(self):
        self.assertEquals(self.get_length('name'), 100)

    def should_have_non_nullable_name(self):
        self.assertFalse(self.is_nullable('name'))

    def should_have_summary(self):
        self.assertEquals(self.Default.summary, self.tag_data.Default.summary)

    def should_have_summary_as_string(self):
        self.assertTrue(self.is_type('summary', self.db.String))

    def should_have_summary_with_length(self):
        self.assertEquals(self.get_length('summary'), 100)

    def should_have_author(self):
        author = self.Default.author
        self.assertEqual(author.id, self.user_data.Default.id)

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
