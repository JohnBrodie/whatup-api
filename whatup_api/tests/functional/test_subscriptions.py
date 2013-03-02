"""subscriptions endpoint test"""
import whatup_api.models as m
from whatup_api.tests.functional import _FunctionalTestCase, _NotFoundTestCase


class WhenGettingSubscriptionsIndex(_FunctionalTestCase):

    endpoint = '/subscriptions'
    expected_status = 200

    def should_return_all_subscriptions(self):
        self.assertEqual(2, len(self.json['objects']))


class WhenGettingSubscriptionByID(_FunctionalTestCase):

    expected_status = 200
    endpoint = '/subscriptions'

    def should_return_users_subscriptions(self):
        user_subs = [1, 2]
        returned_subs = [int(sub['id']) for sub in self.json['objects']]
        self.assertEquals(set(user_subs), set(returned_subs))


class WhenGettingSubscriptionWithInvalidID(_NotFoundTestCase):
    endpoint = '/subscriptions/999'


class WhenCreatingValidSubscription(_FunctionalTestCase):

    endpoint = '/subscriptions'
    expected_status = 201
    post_data = {}
    new_id = 3

    def should_return_new_subscription_id(self):
        self.assertEquals(self.new_id, self.json['id'])

    def should_create_subscription(self):
        new_subscription = self.db.session.query(m.Subscription) \
            .filter_by(id=self.new_id).one()
        self.assertIsNotNone(new_subscription)

# TODO: Is broken until next release of restless, unless we patch
#class WhenCreatingSubscriptionWithInvalidSubscribee(_FunctionalTestCase):
#
#    endpoint = '/subscriptions'
#    expected_status = 400
#    post_data = {'subscribee': 999}
#
#    def should_return_validation_error(self):
#        self.assertEqual(self.json['validation_errors']['user_id'],
#                         'Must specify user_id')


#class WhenCreatingSubscriptionWithInvalidUser(_FunctionalTestCase):
#
#    endpoint = '/subscriptions'
#    expected_status = 400
#    post_data = {'user': 999}
#
#    def should_return_validation_error(self):
#        self.assertTrue('validation_errors' in self.json)


class WhenDeletingSubscriptions(_FunctionalTestCase):

    endpoint = '/subscriptions/1'
    expected_status = 204
    delete = True

    def should_not_remove_model(self):
        query = self.db.session.query(m.Subscription) \
            .filter_by(id=1)
        self.assertEqual(query.count(), 1)

    def should_set_is_deleted(self):
        query = self.db.session.query(m.Subscription) \
            .filter_by(id=1).one()
        self.assertEqual(query.is_deleted, True)


class WhenEditingSubscriptions(_FunctionalTestCase):

    endpoint = '/subscriptions/1'
    expected_status = 200
    put_data = {'user': 2}

    def should_return_edited_subscription_data(self):
        self.assertEqual(self.put_data['user'], self.json['user'])


class WhenEditingSubscriptionWithInvalidID(_FunctionalTestCase):

    endpoint = '/subscriptions/999'
    expected_status = 404
    expected_content_type = 'application/json'
    put_data = {'user': 2}

    def should_return_404(self):
        self.assertEqual(self.json['error'], '404 Not Found')
