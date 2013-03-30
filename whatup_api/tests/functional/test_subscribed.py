"""Subscribed endpoint test"""
from whatup_api.tests.functional import _FunctionalTestCase


class WhenGettingSubscribed(_FunctionalTestCase):

    endpoint = '/subscribed'
    expected_status = 200

    def should_return_matching_post_body(self):
        self.assertEqual(self.json['objects'][0]['body'],
                         self.fixture_data.PostData.Default['body'])

    def should_return_matching_posts_as_list(self):
        self.assertIsInstance(self.json['objects'], list)
