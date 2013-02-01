"""Test case for Revision model"""
from whatup_api.tests.unit.models import _ModelTestCase


class RevisionModelTestCase(_ModelTestCase):
    """Tests for Revision model"""

    model_name = 'Revision'


class DescribeRevisionModel(RevisionModelTestCase):

    def should_have_body(self):
        self.assertEquals(self.Default.body, self.revision_data.Default.body)

    def should_have_body_as_string(self):
        self.assertTrue(self.is_type('body', self.db.String))

    def should_have_body_with_length(self):
        self.assertEquals(self.get_length('body'), 1000)

    def should_have_non_nullable_body(self):
        self.assertFalse(self.is_nullable('body'))

    def should_have_non_nullable_user(self):
        self.assertFalse(self.is_nullable('user_id'))

    def should_have_nullable_post(self):
        self.assertTrue(self.is_nullable('post_id'))

    def should_have_post(self):
        post = self.Default.post
        self.assertEqual(post.id, self.post_data.Default.id)

    def should_have_author(self):
        author = self.Default.author
        self.assertEqual(author.id, self.user_data.Default.id)
