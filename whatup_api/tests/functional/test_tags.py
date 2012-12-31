"""tags endpoint test"""
import whatup_api.models as m
from whatup_api.tests.functional import FunctionalTestCase


class WhenGettingTagsIndex(FunctionalTestCase):

    endpoint = '/api/tags'
    expected_status = 200

    def should_return_all_tags(self):
        self.assertEqual(2, len(self.json['objects']))


class WhenGettingTagByID(FunctionalTestCase):

    expected_status = 200
    endpoint = '/api/tags/1'

    def should_return_tag_summary(self):
        self.assertEqual(self.json['summary'],
                         self.fixture_data.TagData.Default.summary)


class WhenGettingTagWithInvalidID(FunctionalTestCase):

    endpoint = '/api/tags/999'
    expected_status = 404

    def should_return_html_notice(self):
        assert '<title>404 Not Found</title>' in self.response.data


class WhenCreatingValidTag(FunctionalTestCase):

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


class WhenCreatingInvalidTag(FunctionalTestCase):

    endpoint = '/api/tags'
    expected_status = 400
    post_data = {'name': None}

    def should_return_validation_error(self):
        self.assertEqual(self.json['validation_errors']['name'],
                         'Must specify name')


# TODO we should probably add an 'inactive' field to everything,
# and delete nothing
class WhenDeletingTags(FunctionalTestCase):
    pass


class WhenEditingTags(FunctionalTestCase):

    endpoint = '/api/tags/1'
    expected_status = 200
    put_data = {'summary': 'new summary here'}

    def should_return_edited_tag_data(self):
        self.assertEqual(self.put_data['summary'], self.json['summary'])


# TODO this breaks flask-restless
#class WhenEditingTagWithInvalidID(FunctionalTestCase):
#
#    endpoint = '/api/tags/999'
#    expected_status = 404
#    put_data = {'bio': 'new bio here'}
#
#    def should_return_html_notice(self):
#        assert '<title>404 Not Found</title>' in self.response.data
