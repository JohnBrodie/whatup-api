"""Test case for User model"""
import whatup_api.models as m
from whatup_api.tests.unit.models import ModelTestCase


class UserModelTestCase(ModelTestCase):
    """Tests for User model"""

    def setUp(self):
        super(UserModelTestCase, self).setUp()
        self.user = self.db.session.query(m.User) \
            .filter_by(id=self.user_data.default.id).one()

    def tearDown(self):
        super(UserModelTestCase, self).tearDown()

    def should_have_id(self):
        self.assertEquals(self.user.id, self.user_data.default.id)

    def should_have_created_at(self):
        self.assertEquals(self.user.created_at,
                          self.user_data.default.created_at)

    def should_have_modified_at(self):
        self.assertEquals(self.user.modified_at,
                          self.user_data.default.modified_at)

    def should_have_name(self):
        self.assertEquals(self.user.name, self.user_data.default.name)

    def should_have_bio(self):
        self.assertEquals(self.user.bio, self.user_data.default.bio)
