"""Test case for User model"""
import whatup_api.models as m
from whatup_api.tests.unit.models import ModelTestCase


class UserModelTestCase(ModelTestCase):
    """Tests for User model"""

    def setUp(self):
        super(UserModelTestCase, self).setUp()
        self.model = m.User
        self.columns, self.relations = self.get_columns_and_relations()

        self.user = self.db.session.query(m.User) \
            .filter_by(id=self.user_data.Default.id).one()
        self.specifies_none = self.db.session.query(m.User) \
            .filter_by(id=self.user_data.SpecifiesNone.id).one()

    def tearDown(self):
        super(UserModelTestCase, self).tearDown()


class DescribeUserModel(UserModelTestCase):
    def should_have_table_name(self):
        self.assertEquals(m.User.__tablename__, 'users')

    def should_have_id_as_pkey(self):
        self.assertTrue(self.is_primary_key('id'))


class DescribeIdColumn(UserModelTestCase):

    def should_have_id(self):
        self.assertEquals(self.user.id, self.user_data.Default.id)

    def should_have_id_as_integer(self):
        self.assertTrue(self.is_type('id', self.db.Integer))

    def should_have_created_at(self):
        self.assertEquals(self.user.created_at,
                          self.user_data.Default.created_at)


class DescribeCreatedAtColumn(UserModelTestCase):

    def should_have_default_created_at(self):
        self.assertTrue(self.compare_time(self.specifies_none.created_at))

    def should_have_created_at_as_datetime(self):
        self.assertTrue(self.is_type('created_at', self.db.DateTime))

    def should_have_non_nullable_created_at(self):
        self.assertFalse(self.is_nullable('created_at'))


class DescribeModifiedAtColumn(UserModelTestCase):

    def should_have_modified_at(self):
        self.assertEquals(self.user.modified_at,
                          self.user_data.Default.modified_at)

    def should_have_modified_at_as_datetime(self):
        self.assertTrue(self.is_type('modified_at', self.db.DateTime))

    def should_have_non_nullable_modified_at(self):
        self.assertFalse(self.is_nullable('modified_at'))

    def should_have_default_modified_at(self):
        self.assertTrue(self.compare_time(self.specifies_none.modified_at))


class DescribeNameColumn(UserModelTestCase):
    def should_have_name(self):
        self.assertEquals(self.user.name, self.user_data.Default.name)

    def should_have_name_as_string(self):
        self.assertTrue(self.is_type('name', self.db.String))

    def should_have_name_with_length(self):
        self.assertEquals(self.get_length('name'), 255)

    def should_have_non_nullable_name(self):
        self.assertFalse(self.is_nullable('name'))

class DescribeAliasColumn(UserModelTestCase):

    def should_have_alias(self):
        self.assertEquals(self.user.alias, self.user_data.Default.alias)

    def should_have_alias_as_string(self):
        self.assertTrue(self.is_type('alias', self.db.String))

    def should_have_alias_with_length(self):
        self.assertEquals(self.get_length('alias'), 255)

    def should_have_nullable_alias(self):
        self.assertEquals(self.specifies_none.alias, None)


class DescribeBioColumn(UserModelTestCase):

    def should_have_bio(self):
        self.assertEquals(self.user.bio, self.user_data.Default.bio)

    def should_have_bio_as_string(self):
        self.assertTrue(self.is_type('bio', self.db.String))

    def should_have_bio_with_length(self):
        self.assertEquals(self.get_length('bio'), 255)

    def should_have_nullable_bio(self):
        self.assertEquals(self.specifies_none.bio, None)


class DescribeSubscriptionRelationship(UserModelTestCase):

    def should_have_subscriptions(self):
        subscriptions = self.user.subscriptions.all()
        self.assertEquals(len(subscriptions), 2)

        for sub in subscriptions:
            self.assertEqual(sub.owner.id, self.user.id)

    def should_have_subscriptions_relation_to_subscription_model(self):
        self.assertEquals(self.has_target('subscriptions'), 'subscriptions')

    def should_have_subscriptions_dynamically_loaded(self):
        self.assertEquals(self.is_lazy('subscriptions'), 'dynamic')

    def should_have_subscriptions_backref_to_owner(self):
        self.assertEquals(self.has_backref('subscriptions'), 'owner')


class DescribeTagsCreatedRelationship(UserModelTestCase):
    def should_have_tags_created(self):
        tags = self.user.tags_created.all()
        self.assertEquals(len(tags), 1)

        for tag in tags:
            self.assertEqual(tag.author.id, self.user.id)

    def should_have_tags_created_relation_to_tags_model(self):
        self.assertEquals(self.has_target('tags_created'), 'tags')

    def should_have_tags_created_dynamically_loaded(self):
        self.assertEquals(self.is_lazy('tags_created'), 'dynamic')

    def should_have_tags_created_backref_to_author(self):
        self.assertEquals(self.has_backref('tags_created'), 'author')


class DescribePostRelationship(UserModelTestCase):

    def should_have_posts(self):
        posts = self.user.posts.all()
        self.assertEquals(len(posts), 2)

        for post in posts:
            self.assertEqual(post.author.id, self.user.id)

    def should_have_posts_relation_to_posts_model(self):
        self.assertEquals(self.has_target('posts'), 'posts')

    def should_have_posts_dynamically_loaded(self):
        self.assertEquals(self.is_lazy('posts'), 'dynamic')

    def should_have_posts_backref_to_author(self):
        self.assertEquals(self.has_backref('posts'), 'author')
