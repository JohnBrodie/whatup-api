""" Functional TestCase Setup """
from json import dumps, loads

from whatup_api.tests import _BaseApiTestCase


class _FunctionalTestCase(_BaseApiTestCase):

    post_headers = [('Content-Type', 'application/json')]
    expected_content_type = 'application/json'

    @classmethod
    def setUpClass(cls):
        super(_FunctionalTestCase, cls).setUpClass()
        cls.response = cls.get_response()
        cls.json = cls.response_to_json(cls.response)

    @classmethod
    def response_to_json(cls, response):
        json = None
        try:
            json = loads(response.data)
        except ValueError:
            pass
        return json

    @classmethod
    def set_openid_key(cls):
        with cls.client.session_transaction() as session:
            session['openid'] = 'openidkey'

    @classmethod
    def remove_openid_key(cls):
        with cls.client.session_transaction() as session:
            if session.get('openid'):
                del session['openid']

    @classmethod
    def get_response(cls, login=True):
        if not hasattr(cls, 'endpoint'):
            return
        response = ''

        with cls.client:
            if login:
                cls.set_openid_key()

            if hasattr(cls, 'filename'):
                response = cls.client.post(
                    cls.endpoint, data=cls.post_data,
                    headers=cls.post_headers)

            elif hasattr(cls, 'post_data'):
                response = cls.client.post(
                    cls.endpoint, data=dumps(cls.post_data),
                    headers=cls.post_headers)

            elif hasattr(cls, 'put_data'):
                response = cls.client.put(
                    cls.endpoint, data=dumps(cls.put_data),
                    headers=cls.post_headers)

            elif hasattr(cls, 'delete'):
                response = cls.client.delete(
                    cls.endpoint, headers=cls.post_headers)

            else:
                response = cls.client.get(cls.endpoint)

        return response

    def should_have_status(self):
        self.assertEqual(self.response.status_code, self.expected_status)

    def should_have_content_type(self):
        self.assertEqual(self.response.content_type, self.expected_content_type)

    def should_not_return_is_deleted(self):
        self.assertNotIn('is_deleted', self.response.data)

    def should_return_302_status_code_if_not_logged_in(self):
        if hasattr(self, 'filename'):
            return

        self.remove_openid_key()
        response = self.get_response(login=False)
        self.assertEqual(response.status_code, 302)

    def should_redirect_if_not_logged_in(self):
        if hasattr(self, 'filename'):
            return
        expected_html = (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 '
            'Final//EN">\n<title>Redirecting...</title>\n<h1>Redirecting...'
            '</h1>\n<p>You should be redirected automatically to target URL: '
            '<a href="/login">/login</a>.  If not click the link.'
        )
        self.remove_openid_key()
        response = self.get_response(login=False)
        self.assertEqual(response.data, expected_html)


class _NotFoundTestCase(_FunctionalTestCase):

    expected_status = 404
    expected_content_type = 'application/json'

    def should_return_not_found_json(self):
        self.assertEqual(self.json['error'],
                         u'404 Not Found')
