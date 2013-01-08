"""subscriptions endpoint test"""
import whatup_api.models as m
from whatup_api.tests.functional import _FunctionalTestCase


class WhenGettingSubscriptionsIndex(_FunctionalTestCase):

    endpoint = '/api/subscriptions'
    expected_status = 200

    def should_return_all_subscriptions(self):
        self.assertEqual(2, len(self.json['objects']))


class WhenGettingSubscriptionByID(_FunctionalTestCase):

    expected_status = 200
    endpoint = '/api/subscriptions/1'

    def should_return_subscription_user_id(self):
        self.assertEqual(self.json['user_id'],
                         self.fixture_data.SubscriptionData.Default.user_id)


class WhenGettingSubscriptionWithInvalidID(_FunctionalTestCase):

    endpoint = '/api/subscriptions/999'
    expected_status = 404
    expected_content_type = 'text/html'

    def should_return_html_notice(self):
        assert '<title>404 Not Found</title>' in self.response.data


class WhenCreatingValidSubscription(_FunctionalTestCase):

    endpoint = '/api/subscriptions'
    expected_status = 201
    post_data = {'user_id': 1}
    new_id = 3

    def should_return_new_subscription_id(self):
        self.assertEquals(self.new_id, self.json['id'])

    def should_create_subscription(self):
        new_subscription = self.db.session.query(m.Subscription) \
            .filter_by(id=self.new_id).one()
        self.assertIsNotNone(new_subscription)


class WhenCreatingSubscriptionWithoutUserId(_FunctionalTestCase):

    endpoint = '/api/subscriptions'
    expected_status = 400
    post_data = {'user_id': None}

    def should_return_validation_error(self):
        self.assertEqual(self.json['validation_errors']['user_id'],
                         'Must specify user_id')


class WhenCreatingSubscriptionWithInvalidUserId(_FunctionalTestCase):

    endpoint = '/api/subscriptions'
    expected_status = 400
    post_data = {'user_id': 999}

    def should_return_validation_error(self):
        self.assertTrue('validation_errors' in self.json)


# TODO we should probably add an 'inactive' field to everything,
# and delete nothing
class WhenDeletingSubscriptions(_FunctionalTestCase):

    endpoint = '/api/posts'
    expected_status = 200


class WhenEditingSubscriptions(_FunctionalTestCase):

    endpoint = '/api/subscriptions/1'
    expected_status = 200
    put_data = {'user_id': 2}

    def should_return_edited_subscription_data(self):
        self.assertEqual(self.put_data['user_id'], self.json['user_id'])


# TODO this breaks flask-restless
#class WhenEditingSubscriptionWithInvalidID(_FunctionalTestCase):
#
#    endpoint = '/api/subscriptions/999'
#    expected_status = 404
#    expected_content_type = 'text/html'
#    put_data = {'bio': 'new bio here'}
#
#    def should_return_html_notice(self):
#        assert '<title>404 Not Found</title>' in self.response.data
