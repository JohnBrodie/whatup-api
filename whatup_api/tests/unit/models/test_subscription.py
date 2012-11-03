"""Test case for Subscription model"""
import whatup_api.models as m
from sqlalchemy.exc import IntegrityError

from whatup_api.tests.unit.models import ModelTestCase




class SubscriptionModelTestCase(ModelTestCase):
    """Tests for Subscription model"""

    def setUp(self):
        super(SubscriptionModelTestCase, self).setUp()
        self.subscription = self.db.session.query(m.Subscription) \
            .filter_by(id=self.subscription_data.Default.id).one()

    def tearDown(self):
        super(SubscriptionModelTestCase, self).tearDown()

    def should_have_id(self):
        self.assertEquals(self.subscription.id,
                          self.subscription_data.Default.id)

    def should_have_created_at(self):
        self.assertEquals(self.subscription.created_at,
                          self.subscription_data.Default.created_at)

    def should_have_modified_at(self):
        self.assertEquals(self.subscription.modified_at,
                          self.subscription_data.Default.modified_at)

    def should_have_user(self):
        self.assertEquals(self.subscription.owner.id,
                          self.user_data.Default.id)

    def should_be_able_to_add_tag(self):
        self.subscription.tag_names.append('test-tag')
        self.assertEquals(self.subscription.tag_names[0], 'test-tag')

    def should_not_be_able_to_add_duplicate_tag(self):
        self.subscription.tag_names.append('test-tag')
        self.subscription.tag_names.append('test-tag')
        self.assertRaisesRegexp(IntegrityError, r'1062', self.db.session.commit) # 1062 = mysql duplicate entry error code
