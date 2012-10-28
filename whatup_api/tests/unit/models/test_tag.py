"""Test case for Tag model"""
import whatup_api.models as m

from whatup_api.tests.unit.models import ModelTestCase


class TagModelTestCase(ModelTestCase):
    """Tests for Tag model"""

    def setUp(self):
        super(TagModelTestCase, self).setUp()
        self.tag = self.db.session.query(m.Tag) \
            .filter_by(id=self.tag_data.default.id).one()

    def tearDown(self):
        super(TagModelTestCase, self).tearDown()

    def should_have_id(self):
        self.assertEquals(self.tag.id, self.tag_data.default.id)

    def should_have_created_at(self):
        self.assertEquals(self.tag.created_at,
                          self.tag_data.default.created_at)

    def should_have_modified_at(self):
        self.assertEquals(self.tag.modified_at,
                          self.tag_data.default.modified_at)

    def should_have_summary(self):
        self.assertEquals(self.tag.summary, self.tag_data.default.summary)

    def should_have_author(self):
        self.assertEquals(self.tag.author.id, self.user_data.default.id)
