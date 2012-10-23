"""Test case for User model"""
import unittest2

import whatup_api.models as m
from whatup_api.tests.unit.models import ModelTestCase
from whatup_api.tests.fixtures.user_data import UserData


class UserModelTestCase(ModelTestCase):
    """Tests for User model"""

    def setUp(self):
        super(UserModelTestCase, self).setUp()
        self.user = self.db.session.query(m.User) \
            .filter_by(id=UserData.default.id).one()

    def tearDown(self):
        super(UserModelTestCase, self).tearDown()

    def should_have_id(self):
        self.assertEquals(self.user.id, UserData.default.id)

    def should_have_created_at(self):
        self.assertEquals(self.user.created_at, UserData.default.created_at)

    def should_have_modified_at(self):
        self.assertEquals(self.user.modified_at, UserData.default.modified_at)

    def should_have_name(self):
        self.assertEquals(self.user.name, UserData.default.name)

    def should_have_bio(self):
        self.assertEquals(self.user.bio, UserData.default.bio)
