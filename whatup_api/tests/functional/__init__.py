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
    def set_openid_key(cls, client):
        with client.session_transaction() as session:
            session['openid'] = 'openidkey'

    @classmethod
    def get_response(cls):
        if not hasattr(cls, 'endpoint'):
            return

        with cls.client as client:
            cls.set_openid_key(client)

            if hasattr(cls, 'filename'):
                cls.response = client.post(
                    cls.endpoint, data=cls.post_data,
                    headers=cls.post_headers)

            elif hasattr(cls, 'post_data'):
                cls.response = client.post(
                    cls.endpoint, data=dumps(cls.post_data),
                    headers=cls.post_headers)

            elif hasattr(cls, 'put_data'):
                cls.response = client.put(
                    cls.endpoint, data=dumps(cls.put_data),
                    headers=cls.post_headers)

            elif hasattr(cls, 'delete'):
                cls.response = client.delete(
                    cls.endpoint, headers=cls.post_headers)

            else:
                cls.response = client.get(cls.endpoint)

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


class _NotFoundTestCase(_FunctionalTestCase):

    expected_status = 404
    expected_content_type = 'application/json'

    def should_return_not_found_json(self):
        self.assertEqual(self.json['error'],
                         u'404 Not Found')
