"""subscriptions endpoint test"""
import whatup_api.models as m
from whatup_api.tests.functional import FunctionalTestCase


class WhenGettingSubscriptionsIndex(FunctionalTestCase):

    endpoint = '/api/subscriptions'
    expected_status = 200

    def should_return_all_subscriptions(self):
        self.assertEqual(2, len(self.json['objects']))


class WhenGettingSubscriptionByID(FunctionalTestCase):

    expected_status = 200
    endpoint = '/api/subscriptions/1'

    def should_return_subscription_user_id(self):
        self.assertEqual(self.json['user_id'],
                         self.fixture_data.SubscriptionData.Default.user_id)


class WhenGettingSubscriptionWithInvalidID(FunctionalTestCase):

    endpoint = '/api/subscriptions/999'
    expected_status = 404

    def should_return_html_notice(self):
        assert '<title>404 Not Found</title>' in self.response.data


class WhenCreatingValidSubscription(FunctionalTestCase):

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


class WhenCreatingInvalidSubscription(FunctionalTestCase):

    endpoint = '/api/subscriptions'
    expected_status = 400
    post_data = {'user_id': 999}

    def should_return_validation_error(self):
        self.assertTrue('validation_errors' in self.json)


# TODO we should probably add an 'inactive' field to everything,
# and delete nothing
class WhenDeletingSubscriptions(FunctionalTestCase):
    pass


class WhenEditingSubscriptions(FunctionalTestCase):

    endpoint = '/api/subscriptions/1'
    expected_status = 200
    put_data = {'user_id': 2}

    def should_return_edited_subscription_data(self):
        self.assertEqual(self.put_data['user_id'], self.json['user_id'])


# TODO this breaks flask-restless
#class WhenEditingSubscriptionWithInvalidID(FunctionalTestCase):
#
#    endpoint = '/api/subscriptions/999'
#    expected_status = 404
#    put_data = {'bio': 'new bio here'}
#
#    def should_return_html_notice(self):
#        assert '<title>404 Not Found</title>' in self.response.data
