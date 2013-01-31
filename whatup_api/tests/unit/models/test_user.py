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

    def should_have_openid(self):
        self.assertEqual(self.Default.openid, self.user_data.Default.openid)

    def should_have_openid_as_string(self):
        self.assertTrue(self.is_type('openid', self.db.String))

    def should_have_openid_with_length(self):
        self.assertEqual(self.get_length('openid'), 255)

    def should_have_nullable_openid(self):
        self.assertEqual(self.SpecifiesNone.openid, None)

    def should_have_subscriptions(self):
        subscriptions = self.Default.subscriptions.all()
        self.assertEquals(len(subscriptions), 2)

        for sub in subscriptions:
            self.assertEqual(sub.owner.id, self.Default.id)

    def should_have_subscriptions_relation_to_subscription_model(self):
        self.assertEquals(self.has_target('subscriptions'), 'subscriptions')

    def should_have_subscriptions_dynamically_loaded(self):
        self.assertEquals(self.is_lazy('subscriptions'), 'dynamic')

    def should_have_subscriptions_backref_to_owner(self):
        self.assertEquals(self.has_backref('subscriptions'), 'owner')

    def should_have_tags_created(self):
        tags = self.Default.tags_created.all()
        self.assertEquals(len(tags), 2)

        for tag in tags:
            self.assertEqual(tag.author.id, self.Default.id)

    def should_have_tags_created_relation_to_tags_model(self):
        self.assertEquals(self.has_target('tags_created'), 'tags')

    def should_have_tags_created_dynamically_loaded(self):
        self.assertEquals(self.is_lazy('tags_created'), 'dynamic')

    def should_have_tags_created_backref_to_author(self):
        self.assertEquals(self.has_backref('tags_created'), 'author')

    def should_have_posts(self):
        posts = self.Default.posts.all()
        self.assertEquals(len(posts), 2)

        for post in posts:
            self.assertEqual(post.author.id, self.Default.id)

    def should_have_posts_relation_to_posts_model(self):
        self.assertEquals(self.has_target('posts'), 'posts')

    def should_have_posts_dynamically_loaded(self):
        self.assertEquals(self.is_lazy('posts'), 'dynamic')

    def should_have_posts_backref_to_author(self):
        self.assertEquals(self.has_backref('posts'), 'author')

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
