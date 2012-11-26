"""Test case for Subscription model"""
import whatup_api.models as m

from whatup_api.tests.unit.models import ModelTestCase


class SubscriptionModelTestCase(ModelTestCase):
    """Tests for Subscription model"""

    def setUp(self):
        super(SubscriptionModelTestCase, self).setUp()
        self.model = m.Subscription
        self.columns, self.relations = self.get_columns_and_relations()

        self.subscription = self.db.session.query(m.Subscription) \
            .filter_by(id=self.subscription_data.Default.id).one()
        self.specifies_none = self.db.session.query(m.Subscription) \
            .filter_by(id=self.subscription_data.SpecifiesNone.id).one()

    def tearDown(self):
        super(SubscriptionModelTestCase, self).tearDown()


class DescribeSubscriptionModel(SubscriptionModelTestCase):
    def should_have_table_name(self):
        self.assertEquals(m.Subscription.__tablename__, 'subscriptions')

    def should_have_id_as_pkey(self):
        self.assertTrue(self.is_primary_key('id'))


class DescribeIdColumn(SubscriptionModelTestCase):
    def should_have_id(self):
        self.assertEquals(self.subscription.id,
                          self.subscription_data.Default.id)

    def should_have_id_as_integer(self):
        self.assertTrue(self.is_type('id', self.db.Integer))


class DescribeCreatedAtColumn(SubscriptionModelTestCase):
    def should_have_default_created_at(self):
        self.assertTrue(self.compare_time(self.specifies_none.created_at))

    def should_have_created_at_as_datetime(self):
        self.assertTrue(self.is_type('created_at', self.db.DateTime))

    def should_have_non_nullable_created_at(self):
        self.assertFalse(self.is_nullable('created_at'))


class DescribeModifiedAtColumn(SubscriptionModelTestCase):
    def should_have_modified_at(self):
        self.assertEquals(self.subscription.modified_at,
                          self.subscription_data.Default.modified_at)

    def should_have_modified_at_as_datetime(self):
        self.assertTrue(self.is_type('modified_at', self.db.DateTime))

    def should_have_non_nullable_modified_at(self):
        self.assertFalse(self.is_nullable('modified_at'))

    def should_have_default_modified_at(self):
        self.assertTrue(self.compare_time(self.specifies_none.modified_at))


class DescribeUserIdColumn(SubscriptionModelTestCase):
    def should_have_user_id(self):
        self.assertEquals(self.subscription.user_id,
                          self.subscription_data.Default.user_id)

    def should_have_user_id_as_integer(self):
        self.assertTrue(self.is_type('user_id', self.db.Integer))

class DescribeUserColumn(SubscriptionModelTestCase):
    def should_have_user(self):
        self.assertEquals(self.subscription.user,
                          self.subscription_data.Default.user)

    def should_have_user_as_integer(self):
        self.assertTrue(self.is_type('user', self.db.Integer))

    def should_have_user_as_nullable(self):
        self.assertTrue(self.is_nullable('user'))

class DescribeOwnerRelationship(SubscriptionModelTestCase):
    def should_have_owner(self):
        owner = self.subscription.owner
        self.assertEqual(owner.id, self.user_data.Default.id)

class DescribeSubscribeeRelationship(SubscriptionModelTestCase):
    def should_have_subscribee(self):
        subscribee = self.subscription.subscribee
        self.assertEqual(subscribee.id, self.user_data.Default.id)

class DescribeTagRelationship(SubscriptionModelTestCase):
    def should_have_tags(self):
        tags = self.subscription.tags.all()
        for tag in tags:
            self.assertEqual(tag.author.id, self.user.id)

    def should_have_tags_relation_to_tags_model(self):
        self.assertEquals(self.has_target('tags'), 'tags')

    def should_have_tags_dynamically_loaded(self):
        self.assertEquals(self.is_lazy('tags'), 'dynamic')

    def should_have_tags_secondary_table(self):
        self.assertEquals(self.has_secondary('tags'), 'substags')
