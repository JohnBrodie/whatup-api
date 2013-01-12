"""tags endpoint test"""
import whatup_api.models as m
from whatup_api.tests.functional import _FunctionalTestCase, _NotFoundTestCase


class WhenGettingTagsIndex(_FunctionalTestCase):

    endpoint = '/api/tags'
    expected_status = 200

    def should_return_all_tags(self):
        self.assertEqual(2, len(self.json['objects']))


class WhenGettingTagByID(_FunctionalTestCase):

    expected_status = 200
    endpoint = '/api/tags/1'

    def should_return_tag_summary(self):
        self.assertEqual(self.json['summary'],
                         self.fixture_data.TagData.Default.summary)


class WhenGettingTagWithInvalidID(_NotFoundTestCase):

    endpoint = '/api/tags/999'


class WhenCreatingValidTag(_FunctionalTestCase):

    endpoint = '/api/tags'
    expected_status = 201
    post_data = {'name': 'name here'}
    new_id = 3

    def should_return_new_tag_id(self):
        self.assertEquals(self.new_id, self.json['id'])

    def should_create_tag(self):
        new_tag = self.db.session.query(m.Tag) \
            .filter_by(id=self.new_id).one()
        self.assertIsNotNone(new_tag)


class WhenCreatingInvalidTag(_FunctionalTestCase):

    endpoint = '/api/tags'
    expected_status = 400
    post_data = {'name': None}

    def should_return_validation_error(self):
        self.assertEqual(self.json['validation_errors']['name'],
                         'Must specify name')


class WhenDeletingTags(_FunctionalTestCase):

    endpoint = '/api/tags/1'
    expected_status = 204
    delete = True

    def should_not_remove_model(self):
        query = self.db.session.query(m.Tag) \
            .filter_by(id=1)
        self.assertEqual(query.count(), 1)

    def should_set_is_deleted(self):
        query = self.db.session.query(m.Tag) \
            .filter_by(id=1).one()
        self.assertEqual(query.is_deleted, True)


class WhenEditingTags(_FunctionalTestCase):

    endpoint = '/api/tags/1'
    expected_status = 200
    put_data = {'summary': 'new summary here'}

    def should_return_edited_tag_data(self):
        self.assertEqual(self.put_data['summary'], self.json['summary'])


# TODO this breaks flask-restless
#class WhenEditingTagWithInvalidID(_FunctionalTestCase):
#
#    endpoint = '/api/tags/999'
#    expected_status = 404
#    expected_content_type = 'text/html'
#    put_data = {'bio': 'new bio here'}
#
#    def should_return_html_notice(self):
#        assert '<title>404 Not Found</title>' in self.response.data
