"""Fixtures for Subscription model"""
from datetime import datetime
from fixture import DataSet

from whatup_api.tests.fixtures.user_data import UserData
from whatup_api.tests.fixtures.tag_data import TagData


class SubscriptionData(DataSet):

    class Default:
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        owner = UserData.Default
        subscribee = UserData.Default
        is_deleted = False
        tags = [TagData.Default, TagData.SpecifiesNone]

    class SpecifiesNone:
        owner = UserData.Default
