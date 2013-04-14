
import whatup_api.models as m
from whatup_api.tests.functional import _FunctionalTestCase, _NotFoundTestCase


class WhenGettingUsersIndex(_FunctionalTestCase):

    endpoint = '/users'
    expected_status = 200

    def should_return_all_users(self):
        self.assertEqual(2, len(self.json['objects']))


class WhenGettingUserByID(_FunctionalTestCase):

    expected_status = 200
    endpoint = '/users/1'

    def should_return_user_body(self):
        self.assertEqual(self.json['bio'],
                         self.fixture_data.UserData.Default.bio)


class WhenGettingUserWithInvalidID(_NotFoundTestCase):

    endpoint = '/users/999'


class WhenCreatingValidUser(_FunctionalTestCase):

    endpoint = '/users'
    expected_status = 201
    post_data = {'alias': 'name here', 'password': 'password'}
    new_id = 3

    def should_return_new_user_id(self):
        self.assertEquals(self.new_id, self.json['id'])

    def should_create_user(self):
        new_user = self.db.session.query(m.User) \
            .filter_by(id=self.new_id).one()
        self.assertIsNotNone(new_user)


class WhenCreatingUserWithoutAdmin(_FunctionalTestCase):

    endpoint = '/users'
    expected_status = 401
    is_admin = False
    post_data = {'alias': 'name here', 'password': 'password'}

    def should_return_login_url(self):
        self.assertEqual(self.json['url'], '/login')

class WhenChangingOtherUserPasswordWithoutAdmin(_FunctionalTestCase):
    endpoint = '/users/1'
    expected_status = 400
    is_admin = False
    put_data = {'password': 'password'}

class WhenChangingOtherUserPasswordWithAdmin(_FunctionalTestCase):
    endpoint = '/users/2'
    expected_status = 200
    is_admin = True
    put_data = {'password': 'password'}

class WhenChangingOwnPasswordWithoutAdmin(_FunctionalTestCase):
    endpoint = '/users/2'
    expected_status = 200
    is_admin = False
    put_data = {'password': 'password'}

class WhenChangingOwnPasswordWithAdmin(_FunctionalTestCase):
    endpoint = '/users/1'
    expected_status = 200
    is_admin = True
    put_data = {'password': 'password'}



class WhenCreatingNullUser(_FunctionalTestCase):

    endpoint = '/users'
    expected_status = 400
    post_data = {'alias': None}


class WhenNewPasswordHasTooFewCharacters(_FunctionalTestCase):

    endpoint = '/users'
    expected_status = 400
    post_data = {'alias': 'username', 'password': 'p'}


class WhenDeletingUsers(_FunctionalTestCase):

    endpoint = '/users/1'
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

    endpoint = '/users/1'
    expected_status = 200
    put_data = {'bio': 'new bio here'}

    def should_return_edited_user_data(self):
        self.assertEqual(self.put_data['bio'], self.json['bio'])


class WhenEditingUserWithoutAdmin(_FunctionalTestCase):

    endpoint = '/users/2'
    expected_status = 200
    put_data = {'is_admin': True}
    is_admin = False

    def should_not_change_is_admin_status(self):
        self.assertEqual(self.json['is_admin'], False)


class WhenEditingUserWithInvalidID(_FunctionalTestCase):

    endpoint = '/users/999'
    expected_status = 404
    expected_content_type = 'application/json'
    put_data = {'bio': 'new bio here'}

    def should_return_404(self):
        self.assertEqual(self.json['error'], '404 Not Found')
