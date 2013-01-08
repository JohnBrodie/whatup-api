"""Test case for Post model"""
from whatup_api.tests.unit.models import _ModelTestCase


class PostModelTestCase(_ModelTestCase):
    """Tests for Post model"""

    model_name = 'Post'


class DescribePostModel(PostModelTestCase):

    def should_have_rev_id(self):
        self.assertEquals(self.Default.rev_id, self.post_data.Default.rev_id)

    def should_have_rev_id_as_integer(self):
        self.assertTrue(self.is_type('rev_id', self.db.Integer))

    def should_have_topic(self):
        self.assertEquals(self.Default.topic, self.post_data.Default.topic)

    def should_have_topic_as_string(self):
        self.assertTrue(self.is_type('topic', self.db.String))

    def should_have_topic_with_length(self):
        self.assertEquals(self.get_length('topic'), 1000)

    def should_have_non_nullable_topic(self):
        self.assertFalse(self.is_nullable('topic'))

    def should_have_body(self):
        self.assertEquals(self.Default.body, self.post_data.Default.body)

    def should_have_body_as_string(self):
        self.assertTrue(self.is_type('body', self.db.String))

    def should_have_body_with_length(self):
        self.assertEquals(self.get_length('body'), 1000)

    def should_have_non_nullable_body(self):
        self.assertFalse(self.is_nullable('body'))

    def should_have_user_id(self):
        self.assertEquals(self.Default.user_id, self.post_data.Default.user_id)

    def should_have_user_id_as_integer(self):
        self.assertTrue(self.is_type('user_id', self.db.Integer))

    def should_have_author(self):
        author = self.Default.author
        self.assertEqual(author.id, self.user_data.Default.id)

    def should_have_tags(self):
        tags = self.Default.tags.all()
        for tag in tags:
            self.assertEqual(tag.author.id, self.user.id)

    def should_have_tags_relation_to_tags_model(self):
        self.assertEquals(self.has_target('tags'), 'tags')

    def should_have_tags_dynamically_loaded(self):
        self.assertEquals(self.is_lazy('tags'), 'dynamic')

    def should_have_tags_secondary_table(self):
        self.assertEquals(self.has_secondary('tags'), 'posttags')
