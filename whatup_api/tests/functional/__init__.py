""" Functional TestCase Setup """
from json import dumps, loads
from mock import Mock, patch

from whatup_api.tests import _BaseApiTestCase

from flask.ext.login import login_user, logout_user

from whatup_api import models as m


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
    def login(cls):
        cls.client.post('/login', data={'username':'Ayush Sobti', 'password':'password'},
                headers=[('Content-Type', 'multipart/form-data')])

    @classmethod
    def logout(cls):
        cls.client.get('/logout')

    @classmethod
    def get_response(cls, login=True):
        if not hasattr(cls, 'endpoint'):
            return
        response = ''

        with cls.client:
            if login:
                cls.login()

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

    @classmethod
    def getKeys(cls, dictIn):
        keys = []
        for key, value in dictIn.iteritems():
            keys.append(key)
            if isinstance(value, dict):
                keys += cls.getKeys(value)
        return keys

    def should_have_status(self):
        self.assertEqual(self.response.status_code, self.expected_status)

    def should_have_content_type(self):
        self.assertEqual(self.response.content_type, self.expected_content_type)

    def should_not_return_is_deleted(self):
        try:
            json = loads(self.response.data)
            self.assertNotIn('is_deleted', self.getKeys(json))
        except ValueError:
            self.assertTrue(True)

    def should_not_return_pw_hash(self):
        try:
            json = loads(self.response.data)
            self.assertNotIn('pw_hash', self.getKeys(json))
        except ValueError:
            self.assertTrue(True)

    def should_return_401_status_code_if_not_logged_in(self):
        self.logout()
        response = self.get_response(login=False)
        self.assertEqual(response.status_code, 401)

    def should_return_json_if_not_logged_in(self):
        expected_content_type = 'application/json'
        self.logout()
        response = self.get_response(login=False)
        self.assertEqual(response.content_type, expected_content_type)

    def should_return_login_url_if_not_logged_in(self):
        expected_url = '/login'
        self.logout()
        response = self.get_response(login=False)
        json_response = self.response_to_json(response)
        self.assertEqual(json_response['url'], expected_url)


class _NotFoundTestCase(_FunctionalTestCase):

    expected_status = 404
    expected_content_type = 'application/json'

    def should_return_not_found_json(self):
        self.assertEqual(self.json['error'],
                         u'404 Not Found')
