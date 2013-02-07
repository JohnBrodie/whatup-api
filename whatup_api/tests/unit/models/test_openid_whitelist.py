"""Test case for OpenIDWhitelist model"""
from whatup_api.tests.unit.models import _ModelTestCase


class OpenIDWhitelistTestCase(_ModelTestCase):
    """Tests for OpenIDWhitelist model"""

    model_name = 'OpenIDWhitelist'


class DescribeOpenIDWhitelistModel(OpenIDWhitelistTestCase):

    def should_have_name(self):
        self.assertEquals(
            self.Default.name,
            self.model_data.Default.name
        )

    def should_have_name_as_string(self):
        self.assertTrue(self.is_type('name', self.db.String))

    def should_have_name_with_length(self):
        self.assertEquals(self.get_length('name'), 255)

    def should_have_non_nullable_name(self):
        self.assertFalse(self.is_nullable('name'))

    def should_have_email(self):
        self.assertEquals(
            self.Default.email,
            self.model_data.Default.email
        )

    def should_have_email_as_string(self):
        self.assertTrue(self.is_type('email', self.db.String))

    def should_have_email_with_length(self):
        self.assertEquals(self.get_length('email'), 100)

    def should_have_non_nullable_email(self):
        self.assertFalse(self.is_nullable('email'))
