""" Functional TestCase Setup """
from json import dumps, loads
from mock import Mock, patch

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
                if hasattr(cls, 'filepath'):
                    try:
                        cls.post_data['file'] = open(cls.filepath)
                    except IOError:
                        cls.post_data['file'] = None

                mock_open = Mock()
                mock_open.info.return_value = {}
                mock_open.headers = {}
                mock_open.read.return_value = 'asdf'
                urlopen = Mock(return_value=mock_open)
                with patch('whatup_api.helpers.app_helpers.urlopen', urlopen):
                    response = cls.client.post(
                        cls.endpoint, data=cls.post_data,
                        headers=cls.post_headers)

            elif ('Content-Type', 'multipart/form-data') in cls.post_headers:
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

    def should_return_401_status_code_if_not_logged_in(self):
        self.remove_openid_key()
        response = self.get_response(login=False)
        self.assertEqual(response.status_code, 401)

    def should_return_json_if_not_logged_in(self):
        expected_content_type = 'application/json'
        self.remove_openid_key()
        response = self.get_response(login=False)
        self.assertEqual(response.content_type, expected_content_type)

    def should_return_login_url_if_not_logged_in(self):
        expected_url = '/login'
        self.remove_openid_key()
        response = self.get_response(login=False)
        json_response = self.response_to_json(response)
        self.assertEqual(json_response['url'], expected_url)


class _NotFoundTestCase(_FunctionalTestCase):

    expected_status = 404
    expected_content_type = 'application/json'

    def should_return_not_found_json(self):
        self.assertEqual(self.json['error'],
                         u'404 Not Found')
