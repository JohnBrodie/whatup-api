"""Fixtures for User model"""
from datetime import datetime
from fixture import DataSet
from fixture.style import NamedDataStyle


class UserData(DataSet):

    class default:
        id = 1
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        name = 'Joe Smith'
        bio = 'A little bit country'
        #subscriptions = SubscriptionData.default
        #tags_created = TagsCreatedData.default
        #tags_used = TagsUsedData.default
