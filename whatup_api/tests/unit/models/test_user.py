"""Test case for User model"""
from whatup_api.exceptions import APIError
import whatup_api.models as m
from whatup_api.tests.unit.models import _ModelTestCase


class UserModelTestCase(_ModelTestCase):
    """Tests for User model"""

    model_name = 'User'


class DescribeUserModel(UserModelTestCase):

    def should_have_name(self):
        self.assertEquals(self.Default.name, self.user_data.Default.name)

    def should_have_name_as_string(self):
        self.assertTrue(self.is_type('name', self.db.String))

    def should_have_name_with_length(self):
        self.assertEquals(self.get_length('name'), 255)

    def should_have_non_nullable_name(self):
        self.assertFalse(self.is_nullable('name'))

    def should_have_alias(self):
        self.assertEquals(self.Default.alias, self.user_data.Default.alias)

    def should_have_alias_as_string(self):
        self.assertTrue(self.is_type('alias', self.db.String))

    def should_have_alias_with_length(self):
        self.assertEquals(self.get_length('alias'), 255)

    def should_have_nullable_alias(self):
        self.assertEquals(self.SpecifiesNone.alias, None)

    def should_have_bio(self):
        self.assertEquals(self.Default.bio, self.user_data.Default.bio)

    def should_have_bio_as_string(self):
        self.assertTrue(self.is_type('bio', self.db.String))

    def should_have_bio_with_length(self):
        self.assertEquals(self.get_length('bio'), 255)

    def should_have_nullable_bio(self):
        self.assertEquals(self.SpecifiesNone.bio, None)

    def should_have_email(self):
        self.assertEqual(self.Default.email, self.user_data.Default.email)

    def should_have_email_as_string(self):
        self.assertTrue(self.is_type('email', self.db.String))

    def should_have_email_with_length(self):
        self.assertEqual(self.get_length('email'), 100)

    def should_have_nullable_email(self):
        self.assertEqual(self.SpecifiesNone.email, None)

    def should_have_pw_hash(self):
        self.assertEqual(self.Default.pw_hash, self.user_data.Default.pw_hash)

    def should_have_pw_hash_as_string(self):
        self.assertTrue(self.is_type('pw_hash', self.db.String))

    def should_have_pw_hash_with_length(self):
        self.assertEqual(self.get_length('pw_hash'), 80)

    def should_have_non_nullable_pw_hash(self):
        self.assertFalse(self.is_nullable('pw_hash'))

    def should_have_is_admin(self):
        self.assertEqual(self.Default.is_admin, self.user_data.Default.is_admin)

    def should_have_is_admin_as_boolean(self):
        self.assertTrue(self.is_type('is_admin', self.db.Boolean))

    def should_have_non_nullable_is_admin(self):
        self.assertFalse(self.is_nullable('is_admin'))

    def should_have_name_validation_return_name(self):
        name = 'name here'
        returned_name = m.User.validate_name(
            m.User(), 'name', name)
        self.assertEqual(returned_name, name)

    def should_raise_error_on_null_name(self):
        with self.assertRaises(APIError) as cm:
            m.User.validate_name(
                m.User(), 'name', None)

        error = cm.exception.errors
        self.assertEqual(error['name'], 'Must specify name')
