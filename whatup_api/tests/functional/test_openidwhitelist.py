""" OpenIDWhitelists endpoint test"""
import json
import whatup_api.models as m
from whatup_api.tests.functional import _FunctionalTestCase, _NotFoundTestCase


class WhenGettingOpenIDWhitelistsIndex(_FunctionalTestCase):

    endpoint = '/api/openidwhitelists'
    expected_status = 200

    def should_return_all_openidwhitelists(self):
        self.assertEqual(2, len(self.json['objects']))


class WhenGettingOpenIDWhitelistByID(_FunctionalTestCase):

    expected_status = 200
    endpoint = '/api/openidwhitelists/1'

    def should_return_openidwhitelist_body(self):
        self.assertEqual(self.json['name'],
                         self.fixture_data.OpenIDWhitelistData.Default.name)

    def should_return_openidwhitelist_email(self):
        self.assertEqual(self.json['email'],
                         self.fixture_data.OpenIDWhitelistData.Default.email)


class WhenGettingOpenIDWhitelistWithInvalidID(_NotFoundTestCase):

    endpoint = '/api/openidwhitelists/999'


class WhenCreatingValidOpenIDWhitelist(_FunctionalTestCase):

    endpoint = '/api/openidwhitelists'
    expected_status = 201
    post_data = {
        'name': 'name here',
        'email': 'ted@example.com',
    }
    new_id = 3

    def should_return_new_openidwhitelist_id(self):
        self.assertEquals(self.new_id, self.json['id'])

    def should_create_openidwhitelist(self):
        new_openidwhitelist = self.db.session.query(m.OpenIDWhitelist).get(self.new_id)
        self.assertIsNotNone(new_openidwhitelist)


class WhenCreatingInvalidOpenIDWhitelist(_FunctionalTestCase):

    endpoint = '/api/openidwhitelists'
    expected_status = 400
    post_data = {'name': None, 'email': 'a@b.cc'}

    def should_return_validation_error(self):
        self.assertTrue('validation_errors' in self.json)


class WhenDeletingOpenIDWhitelists(_FunctionalTestCase):

    expected_status = 204
    endpoint = '/api/openidwhitelists/1'
    delete = True

    def should_not_remove_model(self):
        query = self.db.session.query(m.OpenIDWhitelist) \
            .filter_by(id=1)
        self.assertEqual(query.count(), 1)

    def should_set_is_deleted(self):
        query = self.db.session.query(m.OpenIDWhitelist).get(1)
        self.assertEqual(query.is_deleted, True)

    def should_not_return_deleted(self):
        response_data = json.loads(self.client.get('/api/openidwhitelists').data)
        self.assertNotEqual(response_data['objects'][0]['id'], 1)


class WhenEditingOpenIDWhitelists(_FunctionalTestCase):

    endpoint = '/api/openidwhitelists/1'
    expected_status = 200
    put_data = {'name': 'new name'}

    def should_return_edited_openidwhitelist_data(self):
        self.assertEqual(self.put_data['name'], self.json['name'])


class WhenEditingOpenIDWhitelistWithInvalidID(_FunctionalTestCase):

    endpoint = '/api/openidwhitelists/999'
    expected_status = 404
    expected_content_type = 'application/json'
    put_data = {'name': 'new name'}

    def should_return_404(self):
        self.assertEqual(self.json['error'], '404 Not Found')
