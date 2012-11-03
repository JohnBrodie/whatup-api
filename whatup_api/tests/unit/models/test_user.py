"""Test case for User model"""
import whatup_api.models as m
from whatup_api.tests.unit.models import ModelTestCase


class UserModelTestCase(ModelTestCase):
    """Tests for User model"""

    def setUp(self):
        super(UserModelTestCase, self).setUp()
        self.user = self.db.session.query(m.User) \
            .filter_by(id=self.user_data.Default.id).one()
        self.specifies_none = self.db.session.query(m.User) \
            .filter_by(id=self.user_data.SpecifiesNone.id).one()

    def tearDown(self):
        super(UserModelTestCase, self).tearDown()

    def should_have_id(self):
        self.assertEquals(self.user.id, self.user_data.Default.id)

    def should_have_created_at(self):
        self.assertEquals(self.user.created_at,
                          self.user_data.Default.created_at)

    def should_have_default_created_at(self):
        self.assertTrue(self.compare_time(self.specifies_none.created_at))

    def should_have_modified_at(self):
        self.assertEquals(self.user.modified_at,
                          self.user_data.Default.modified_at)

    def should_have_default_modified_at(self):
        self.assertTrue(self.compare_time(self.specifies_none.modified_at))

    def should_have_name(self):
        self.assertEquals(self.user.name, self.user_data.Default.name)

    def should_have_bio(self):
        self.assertEquals(self.user.bio, self.user_data.Default.bio)

    def should_have_subscriptions(self):
        subscriptions = self.user.subscriptions.all()
        self.assertEquals(len(subscriptions), 2)

        for sub in subscriptions:
            self.assertEqual(sub.owner.id, self.user.id)
