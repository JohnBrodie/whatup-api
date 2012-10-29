"""Test case for Post model"""
import whatup_api.models as m

from whatup_api.tests.unit.models import ModelTestCase


class PostModelTestCase(ModelTestCase):
    """Tests for Post model"""

    def setUp(self):
        super(PostModelTestCase, self).setUp()
        self.post = self.db.session.query(m.Post) \
            .filter_by(id=self.post_data.default.id).one()

    def tearDown(self):
        super(PostModelTestCase, self).tearDown()

    def should_have_id(self):
        self.assertEquals(self.post.id, self.post_data.default.id)

    def should_have_rev_id(self):
        self.assertEquals(self.post.rev_id, self.post_data.default.rev_id)

    def should_have_created_at(self):
        self.assertEquals(self.post.created_at,
                          self.post_data.default.created_at)

    def should_have_modified_at(self):
        self.assertEquals(self.post.modified_at,
                          self.post_data.default.modified_at)

    def should_have_topic(self):
        self.assertEquals(self.post.topic, self.post_data.default.topic)

    def should_have_body(self):
        self.assertEquals(self.post.body, self.post_data.default.body)

    def should_have_author(self):
        self.assertEquals(self.post.author.id, self.user_data.default.id)