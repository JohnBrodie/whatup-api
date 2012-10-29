"""Fixtures for Subscription model"""
from datetime import datetime
from fixture import DataSet

from whatup_api.tests.fixtures.user_data import UserData


class SubscriptionData(DataSet):

    class default:
        created_at = datetime(2001, 10, 10)
        modified_at = datetime(2001, 10, 11)
        owner = UserData.default