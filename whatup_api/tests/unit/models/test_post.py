"""Test case for Post model"""
import whatup_api.models as m
from sqlalchemy.exc import IntegrityError

from whatup_api.tests.unit.models import ModelTestCase


class PostModelTestCase(ModelTestCase):
    """Tests for Post model"""

    def setUp(self):
        super(PostModelTestCase, self).setUp()
        self.post = self.db.session.query(m.Post) \
            .filter_by(id=self.post_data.Default.id).one()

    def tearDown(self):
        super(PostModelTestCase, self).tearDown()

    def should_have_id(self):
        self.assertEquals(self.post.id, self.post_data.Default.id)

    def should_have_rev_id(self):
        self.assertEquals(self.post.rev_id, self.post_data.Default.rev_id)

    def should_have_created_at(self):
        self.assertEquals(self.post.created_at,
                          self.post_data.Default.created_at)

    def should_have_modified_at(self):
        self.assertEquals(self.post.modified_at,
                          self.post_data.Default.modified_at)

    def should_have_topic(self):
        self.assertEquals(self.post.topic, self.post_data.Default.topic)

    def should_have_body(self):
        self.assertEquals(self.post.body, self.post_data.Default.body)

    def should_have_author(self):
        self.assertEquals(self.post.author.id, self.user_data.Default.id)

    def should_be_able_to_add_tag(self):
        self.post.tag_names.append('test-tag')
        self.assertEquals(self.post.tag_names[0], 'test-tag')

    def should_not_be_able_to_add_duplicate_tag(self):
        self.post.tag_names.append('test-tag')
        self.post.tag_names.append('test-tag')
        self.assertRaisesRegexp(IntegrityError, r'1062', self.db.session.commit) # 1062 = mysql duplicate entry error code
