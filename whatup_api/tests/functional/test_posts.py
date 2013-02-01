""" Posts endpoint test"""
import json
import whatup_api.models as m
from whatup_api.tests.functional import _FunctionalTestCase, _NotFoundTestCase


class WhenGettingPostsIndex(_FunctionalTestCase):

    endpoint = '/api/posts'
    expected_status = 200

    def should_return_all_posts(self):
        self.assertEqual(2, len(self.json['objects']))


class WhenGettingPostByID(_FunctionalTestCase):

    expected_status = 200
    endpoint = '/api/posts/1'

    def should_return_post_body(self):
        self.assertEqual(self.json['body'],
                         self.fixture_data.PostData.Default.body)


class WhenGettingPostWithInvalidID(_NotFoundTestCase):

    endpoint = '/api/posts/999'


class WhenCreatingValidPost(_FunctionalTestCase):

    endpoint = '/api/posts'
    expected_status = 201
    post_data = {'body': 'body here'}
    new_id = 3

    def should_return_new_post_id(self):
        self.assertEquals(self.new_id, self.json['id'])

    def should_create_post(self):
        new_post = self.db.session.query(m.Post) \
            .filter_by(id=self.new_id).one()
        self.assertIsNotNone(new_post)


class WhenCreatingInvalidPost(_FunctionalTestCase):

    endpoint = '/api/posts'
    expected_status = 400
    post_data = {'body': None}

    def should_return_validation_error(self):
        self.assertTrue('validation_errors' in self.json)


class WhenDeletingPosts(_FunctionalTestCase):

    expected_status = 204
    endpoint = '/api/posts/1'
    delete = True

    def should_not_remove_model(self):
        query = self.db.session.query(m.Post) \
            .filter_by(id=1)
        self.assertEqual(query.count(), 1)

    def should_set_is_deleted(self):
        query = self.db.session.query(m.Post) \
            .filter_by(id=1).one()
        self.assertEqual(query.is_deleted, True)

    def should_not_return_deleted(self):
        response_data = json.loads(self.client.get('/api/posts').data)
        self.assertNotEqual(response_data['objects'][0]['id'], 1)


class WhenEditingPosts(_FunctionalTestCase):

    endpoint = '/api/posts/1'
    expected_status = 200
    put_data = {'body': 'new body here',
                'tags': []}

    def should_return_edited_post_data(self):
        self.assertEqual(self.put_data['body'], self.json['body'])


class WhenEditingPostWithInvalidID(_FunctionalTestCase):

    endpoint = '/api/posts/999'
    expected_status = 404
    expected_content_type = 'application/json'
    put_data = {'body': 'new body here',
                'tags': []}

    def should_return_404(self):
        self.assertEqual(self.json['error'], '404 Not Found')
