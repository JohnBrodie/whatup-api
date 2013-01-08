"""Test case for Subscription model"""
from whatup_api.exceptions import APIError
import whatup_api.models as m

from whatup_api.tests.unit.models import _ModelTestCase


class SubscriptionModelTestCase(_ModelTestCase):
    """Tests for Subscription model"""

    model_name = 'Subscription'


class DescribeSubscriptionModel(SubscriptionModelTestCase):

    def should_have_user_id(self):
        self.assertEquals(self.Default.user_id,
                          self.subscription_data.Default.user_id)

    def should_have_user_id_as_integer(self):
        self.assertTrue(self.is_type('user_id', self.db.Integer))

    def should_have_non_nullable_user_id(self):
        self.assertFalse(self.is_nullable('user_id'))

    def should_have_user(self):
        self.assertEquals(self.Default.user,
                          self.subscription_data.Default.user)

    def should_have_user_as_integer(self):
        self.assertTrue(self.is_type('user', self.db.Integer))

    def should_have_user_as_nullable(self):
        self.assertTrue(self.is_nullable('user'))

    def should_have_owner(self):
        owner = self.Default.owner
        self.assertEqual(owner.id, self.user_data.Default.id)

    def should_have_subscribee(self):
        subscribee = self.Default.subscribee
        self.assertEqual(subscribee.id, self.user_data.Default.id)

    def should_have_tags(self):
        tags = self.Default.tags.all()
        for tag in tags:
            self.assertEqual(tag.author.id, self.user.id)

    def should_have_tags_relation_to_tags_model(self):
        self.assertEquals(self.has_target('tags'), 'tags')

    def should_have_tags_dynamically_loaded(self):
        self.assertEquals(self.is_lazy('tags'), 'dynamic')

    def should_have_tags_secondary_table(self):
        self.assertEquals(self.has_secondary('tags'), 'substags')

    def should_have_user_id_validation_return_user_id(self):
        user_id = 5
        returned_user_id = m.Subscription.validate_user_id(
            m.Subscription(), 'user_id', user_id)
        self.assertEqual(returned_user_id, user_id)

    def should_raise_error_on_null_user_id(self):
        with self.assertRaises(APIError) as cm:
            m.Subscription.validate_user_id(
                m.Subscription(), 'user_id', None)

        error = cm.exception.errors
        self.assertEqual(error['user_id'], 'Must specify user_id')
