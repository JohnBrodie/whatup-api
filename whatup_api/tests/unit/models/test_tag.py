"""Test case for Tag model"""
import unittest2

import whatup_api.models as m
from whatup_api.tests.unit.models import ModelTestCase
from whatup_api.tests.fixtures.tag_data import TagData


class TagModelTestCase(ModelTestCase):
    """Tests for Tag model"""

    def setUp(self):
        super(TagModelTestCase, self).setUp()
        self.tag = self.db.session.query(m.Tag) \
            .filter_by(id=TagData.default.id).one()

    def tearDown(self):
        super(TagModelTestCase, self).tearDown()

    def should_have_id(self):
        self.assertEquals(self.tag.id, TagData.default.id)

    def should_have_created_at(self):
        self.assertEquals(self.tag.created_at, TagData.default.created_at)

    def should_have_modified_at(self):
        self.assertEquals(self.tag.modified_at, TagData.default.modified_at)

    def should_have_summary(self):
        self.assertEquals(self.tag.summary, TagData.default.summary)

    def should_have_author(self):
        pass  # TODO
