"""users endpoint test"""
import whatup_api.models as m
from whatup_api.tests.functional import _FunctionalTestCase


class WhenGettingUsersIndex(_FunctionalTestCase):

    endpoint = '/api/users'
    expected_status = 200

    def should_return_all_users(self):
        self.assertEqual(2, len(self.json['objects']))


class WhenGettingUserByID(_FunctionalTestCase):

    expected_status = 200
    endpoint = '/api/users/1'

    def should_return_user_body(self):
        self.assertEqual(self.json['bio'],
                         self.fixture_data.UserData.Default.bio)


class WhenGettingUserWithInvalidID(_FunctionalTestCase):

    endpoint = '/api/users/999'
    expected_status = 404
    expected_content_type = 'text/html'

    def should_return_html_notice(self):
        assert '<title>404 Not Found</title>' in self.response.data


class WhenCreatingValidUser(_FunctionalTestCase):

    endpoint = '/api/users'
    expected_status = 201
    post_data = {'name': 'name here'}
    new_id = 3

    def should_return_new_user_id(self):
        self.assertEquals(self.new_id, self.json['id'])

    def should_create_user(self):
        new_user = self.db.session.query(m.User) \
            .filter_by(id=self.new_id).one()
        self.assertIsNotNone(new_user)


class WhenCreatingInvalidUser(_FunctionalTestCase):

    endpoint = '/api/users'
    expected_status = 400
    post_data = {'name': None}

    def should_return_validation_error(self):
        self.assertEqual(self.json['validation_errors']['name'],
                         'Must specify name')


class WhenDeletingUsers(_FunctionalTestCase):

    endpoint = '/api/users/1'
    expected_status = 204
    delete = True

    def should_not_remove_model(self):
        query = self.db.session.query(m.User) \
            .filter_by(id=1)
        self.assertEqual(query.count(), 1)

    def should_set_is_deleted(self):
        query = self.db.session.query(m.User) \
            .filter_by(id=1).one()
        self.assertEqual(query.is_deleted, True)


class WhenEditingUsers(_FunctionalTestCase):

    endpoint = '/api/users/1'
    expected_status = 200
    put_data = {'bio': 'new bio here'}

    def should_return_edited_user_data(self):
        self.assertEqual(self.put_data['bio'], self.json['bio'])


# TODO this breaks flask-restless
#class WhenEditingUserWithInvalidID(_FunctionalTestCase):
#
#    endpoint = '/api/users/999'
#    expected_status = 404
#   expected_content_type = 'text/html'
#    put_data = {'bio': 'new bio here'}
#
#    def should_return_html_notice(self):
#        assert '<title>404 Not Found</title>' in self.response.data
