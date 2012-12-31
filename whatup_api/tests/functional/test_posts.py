""" Posts endpoint test"""
import whatup_api.models as m
from whatup_api.tests.functional import FunctionalTestCase


class WhenGettingPostsIndex(FunctionalTestCase):

    endpoint = '/api/posts'
    expected_status = 200

    def should_return_all_posts(self):
        self.assertEqual(2, len(self.json['objects']))


class WhenGettingPostByID(FunctionalTestCase):

    expected_status = 200
    endpoint = '/api/posts/1'

    def should_return_post_body(self):
        self.assertEqual(self.json['body'],
                         self.fixture_data.PostData.Default.body)


class WhenGettingPostWithInvalidID(FunctionalTestCase):

    endpoint = '/api/posts/999'
    expected_status = 404

    def should_return_html_notice(self):
        assert '<title>404 Not Found</title>' in self.response.data


class WhenCreatingValidPost(FunctionalTestCase):

    endpoint = '/api/posts'
    expected_status = 201
    post_data = {'body': 'body here',
                 'user_id': 1}
    new_id = 3

    def should_return_new_post_id(self):
        self.assertEquals(self.new_id, self.json['id'])

    def should_create_post(self):
        new_post = self.db.session.query(m.Post) \
            .filter_by(id=self.new_id).one()
        self.assertIsNotNone(new_post)


class WhenCreatingInvalidPost(FunctionalTestCase):

    endpoint = '/api/posts'
    expected_status = 400
    post_data = {'body': 'body here',
                 'user_id': 999}

    def should_return_validation_error(self):
        self.assertTrue('validation_errors' in self.json)


# TODO we should probably add an 'inactive' field to everything,
# and delete nothing
class WhenDeletingPosts(FunctionalTestCase):
    pass


class WhenEditingPosts(FunctionalTestCase):

    endpoint = '/api/posts/1'
    expected_status = 200
    put_data = {'body': 'new body here',
                'user_id': 1, 'tags': []}

    def should_return_edited_post_data(self):
        self.assertEqual(self.put_data['body'], self.json['body'])


# TODO this breaks flask-restless
#class WhenEditingPostWithInvalidID(FunctionalTestCase):
#
#    endpoint = '/api/posts/999'
#    expected_status = 404
#    put_data = {'body': 'new body here',
#                'user_id': 1, 'tags': []}
#
#    def should_return_html_notice(self):
#        assert '<title>404 Not Found</title>' in self.response.data
