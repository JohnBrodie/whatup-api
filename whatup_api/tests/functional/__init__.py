""" Functional TestCase Setup """
from json import dumps, loads

from whatup_api.tests import _BaseApiTestCase


class _FunctionalTestCase(_BaseApiTestCase):

    post_headers = [('Content-Type', 'application/json')]
    expected_content_type = 'application/json'

    @classmethod
    def setUpClass(cls):
        super(_FunctionalTestCase, cls).setUpClass()
        cls.get_response()

    @classmethod
    def get_response(cls):
        if not hasattr(cls, 'endpoint'):
            return
        if hasattr(cls, 'post_data'):
            cls.response = cls.client.post(
                cls.endpoint, data=dumps(cls.post_data),
                headers=cls.post_headers)

        elif hasattr(cls, 'put_data'):
            cls.response = cls.client.put(
                cls.endpoint, data=dumps(cls.put_data),
                headers=cls.post_headers)

        elif hasattr(cls, 'delete'):
            cls.response = cls.client.delete(
                cls.endpoint, headers=cls.post_headers)

        else:
            cls.response = cls.client.get(cls.endpoint)

        try:
            cls.json = loads(cls.response.data)
        except ValueError:
            cls.json = None

    def should_have_status(self):
        self.assertEqual(self.response.status_code, self.expected_status)

    def should_have_content_type(self):
        self.assertEqual(self.response.content_type, self.expected_content_type)

    def should_not_return_is_deleted(self):
        self.assertNotIn('is_deleted', self.response.data)
