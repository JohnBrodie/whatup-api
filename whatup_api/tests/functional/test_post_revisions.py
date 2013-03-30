"""Post-revisions endpoint test"""
from whatup_api.tests.functional import _FunctionalTestCase


class WhenGettingPostRevisions(_FunctionalTestCase):

    endpoint = '/posts/1/revisions'
    expected_status = 200

    def should_return_number_of_results(self):
        self.assertEqual(self.json['num_results'], 2)


class WhenGettingInvalidPostRevision(_FunctionalTestCase):

    endpoint = '/posts/999/revisions'
    expected_status = 400

    def should_return_error(self):
        expected_error_msg = 'There is no post with id 999'
        self.assertEqual(self.json['error'], expected_error_msg)
